import re
import unicodedata

from django.contrib.postgres.search import SearchQuery, SearchRank
from django.db import connection, models
from django.db.models import F

# This is some complex SQL. Its job is to make a tsvector
# (https://www.postgresql.org/docs/current/datatype-textsearch.html#DATATYPE-TSVECTOR)
# from a list of names. Each name is split up and weighted differently:
# last names are weight 'A', first names 'B' and other names are 'C'.
# This allows us to tune how results are weighted later on when searching.
# Typically, surnames are better to rank by, followed by first names.
# The code is made more complex by the fact that we have two sources of name
# fields: `ynr_person_name` and the `people` object.
POPULATE_NAME_SEARCH_COLUMN_SQL = """
    UPDATE leaflets_leaflet
    SET name_search_vector = subquery.name_search_vector
    FROM (
        SELECT
            id,
            COALESCE(
                (
                    SELECT
                        -- For each name, split it up and add weights
                        STRING_AGG(
                            (
                                SETWEIGHT(TO_TSVECTOR('simple', SPLIT_PART(name, ' ', 1)), 'B') ||
                                SETWEIGHT(TO_TSVECTOR('simple', REGEXP_REPLACE(name, '^.* ', '')), 'A') ||
                                SETWEIGHT(TO_TSVECTOR('simple', name), 'C')
                            )::TEXT,
                            ' '
                        )::TSVECTOR
                    FROM (
                        -- A list of people names
                        SELECT DISTINCT unnest(
                            COALESCE(
                                ARRAY_APPEND(
                                    (
                                        -- Get all the person names from the `people` object
                                        SELECT ARRAY_AGG(people_data->'person'->>'name')
                                        FROM jsonb_each(ll.people) AS people_entry(key, people_data)
                                        WHERE people_data->'person'->>'name' IS NOT NULL
                                    ),
                                    -- add to this the ynr_person_name
                                    ll.ynr_person_name
                                ),
                                ARRAY[]::TEXT[]
                            )
                        ) AS name
                    ) AS unique_names
                ),
                ''::tsvector
            ) AS name_search_vector
        FROM leaflets_leaflet ll
    ) AS subquery
    WHERE leaflets_leaflet.id = subquery.id;
"""

# This does more or less the same as `POPULATE_NAME_SEARCH_COLUMN_SQL` but
# sets up a trigger to update the search vector when a row is updated.
NAME_SEARCH_TRIGGER_SQL = """
    DROP FUNCTION IF EXISTS leaflet_person_name_search_trigger() CASCADE;
    CREATE FUNCTION leaflet_person_name_search_trigger() RETURNS trigger AS $$
    DECLARE
        json_name TEXT;
    BEGIN
        json_name := (
            SELECT people_data->'person'->>'name'
            FROM JSONB_EACH(new.people) AS people_entry(key, people_data)
            LIMIT 1
        );
    
        new.name_search_vector := (
            SELECT
            COALESCE(
                (
                    SELECT
                        STRING_AGG(
                            (
                                SETWEIGHT(TO_TSVECTOR('simple', SPLIT_PART(name, ' ', 1)), 'B') ||
                                SETWEIGHT(TO_TSVECTOR('simple', REGEXP_REPLACE(name, '^.* ', '')), 'A') ||
                                SETWEIGHT(TO_TSVECTOR('simple', name), 'C')
                            )::TEXT,
                            ' '
                        )::TSVECTOR
                    FROM (
                        SELECT DISTINCT UNNEST(
                            COALESCE(
                                ARRAY_APPEND(
                                    (
                                        SELECT ARRAY_AGG(people_data->'person'->>'name')
                                        FROM JSONB_EACH(new.people) AS people_entry(key, people_data)
                                        WHERE people_data->'person'->>'name' IS NOT NULL
                                    ),
                                    new.ynr_person_name
                                ),
                                ARRAY[]::TEXT[]
                            )
                        ) AS name
                    ) AS unique_names
                ),
                ''::tsvector
            )
        );
    
        RETURN new;
    END;
    $$ LANGUAGE plpgsql;
    DROP TRIGGER IF EXISTS tsvectorupdate ON leaflets_leaflet CASCADE;
    CREATE TRIGGER tsvectorupdate BEFORE INSERT OR UPDATE
        ON leaflets_leaflet FOR EACH ROW EXECUTE PROCEDURE leaflet_person_name_search_trigger();
"""


class LeafletQuerySet(models.query.QuerySet):
    def _run_sql(self, SQL):
        with connection.cursor() as cursor:
            cursor.execute(SQL)

    def update_name_search(self):
        self._run_sql(POPULATE_NAME_SEARCH_COLUMN_SQL)

    def update_name_search_trigger(self):
        self._run_sql(NAME_SEARCH_TRIGGER_SQL)

    def search_person_by_name(self, name: str) -> "models.query.QuerySet":
        """
        Take a string and turn it into a Django query that uses PostgresSQLs full
        text search.

        This function manages query parsing, and prevents the user passing in
        search logic.

        """
        # Normalize to ASCII and remove non-alpha charictors on the query side.
        # This has already been done in the indexed data
        name = (
            unicodedata.normalize("NFKD", name)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
        name = name.lower()
        name = re.sub(r"[^a-z ]", " ", name)
        name = " ".join(name.strip().split())
        if not name:
            return self.none()

        # Construct a query that weights an exact match on the name by
        # ANDing each element
        and_name = " & ".join(name.split(" "))
        # Now OR each part together
        or_name = " | ".join(name.split(" "))
        # Combine the AND and OR names. This means we find exact matches
        # above other similar names
        name = f"({and_name}) | ({or_name})"
        name = name.strip()

        # config="simple" is important here. Using 'english' automatically
        # removes 'stop words' like "the" and "an".
        #
        # This is normally useful when searching, but loads of English names also
        # contain stop words.
        #
        # We've had bug reports where the name "will" isn't returned, and this is
        # because "will" is also a common English word.
        #
        # Using 'simple' means no stop-words are removed at index time or search
        # time.
        query = SearchQuery(name, search_type="raw", config="simple")
        return (
            self.filter(name_search_vector=query)
            .annotate(vector=F("name_search_vector"))
            .annotate(
                rank=SearchRank(
                    F("vector"),
                    query,
                    cover_density=True,
                    # Alter the default weights of the fields
                    # Taken from tuning YNR. Use these to alter
                    # how 'heavy' each field is, and therefore how
                    # relevant it is to a search query
                    weights=[
                        0.1,  # The 'A' field, or last name
                        0.3,  # The 'B' field, or first name
                        0.4,  # The 'C' field, or middle names
                        1.0,  # The 'D' field, other (not currently used)
                    ],
                )
            )
            .order_by("-rank")
        )
