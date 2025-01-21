from leaflets.models import Leaflet


def test_search_trigger(db):
    """
    Migrations add a trigger to update the `name_search_vector` field on
    model save.

    Test that this is installed and working
    """
    leaflet = Leaflet.objects.create(
        name_search_vector=None, ynr_person_name="Legitimate First"
    )
    leaflet.refresh_from_db()
    assert leaflet.name_search_vector == "'first':2A,4C 'legitimate':1B,3C"
    assert Leaflet.objects.search_person_by_name("legitimate").count() == 1


def test_search_index_doesnt_duplicate_name(db):
    """
    We can be in a situation where we have content in the `ynr_person_name`
    field and the `people` field. We only want to index one name in the
    `name_search_vector` field.

    """
    leaflet = Leaflet.objects.create(ynr_person_name="Legitimate First")
    leaflet.refresh_from_db()
    assert leaflet.name_search_vector == "'first':2A,4C 'legitimate':1B,3C"

    leaflet.people = {
        "1": {
            "person": {
                "id": 123,
                "url": "https://candidates.democracyclub.org.uk/api/next/people/123/",
                "name": "Legitimate First",
            }
        }
    }

    leaflet.save()
    leaflet.refresh_from_db()
    assert leaflet.name_search_vector == "'first':2A,4C 'legitimate':1B,3C"


def test_search_indexes_both_fields(db):
    """
    We can be in a situation where we have content in the `ynr_person_name`
    field and the `people` field. Make sure we add both sources into one
    field.

    """
    leaflet = Leaflet.objects.create(ynr_person_name="Legitimate First")
    leaflet.refresh_from_db()
    assert leaflet.name_search_vector == "'first':2A,4C 'legitimate':1B,3C"

    leaflet.people = {
        "1": {
            "person": {
                "id": 123,
                "url": "https://candidates.democracyclub.org.uk/api/next/people/123/",
                "name": "Fettle Dodgast",
            }
        }
    }

    leaflet.save()
    leaflet.refresh_from_db()
    assert (
        leaflet.name_search_vector
        == "'dodgast':2A,4C 'fettle':1B,3C 'first':2A,4C 'legitimate':1B,3C"
    )


def test_search_indexes_all_json_people(db):
    """
    We can store more than one person in the `people` field.

    Make sure they're all indexed.

    """
    leaflet = Leaflet.objects.create()

    leaflet.people = {
        "1": {
            "person": {
                "id": 123,
                "url": "https://candidates.democracyclub.org.uk/api/next/people/123/",
                "name": "Legitimate First",
            }
        },
        "2": {
            "person": {
                "id": 456,
                "url": "https://candidates.democracyclub.org.uk/api/next/people/456/",
                "name": "Fettle Dodgast",
            }
        },
    }

    leaflet.save()
    leaflet.refresh_from_db()
    assert (
        leaflet.name_search_vector
        == "'dodgast':2A,4C 'fettle':1B,3C 'first':2A,4C 'legitimate':1B,3C"
    )


def test_search_indexes_middle_names(db):
    """
    Middname names should be a lower ranking

    """
    leaflet = Leaflet.objects.create(ynr_person_name="Legitimate Leggy First")
    leaflet.refresh_from_db()
    assert (
        leaflet.name_search_vector
        == "'first':2A,5C 'leggy':4C 'legitimate':1B,3C"
    )


def test_search_query(db):
    """
    Ensure we can find leaflets by name

    """
    Leaflet.objects.create(ynr_person_name="Legitimate First")
    assert Leaflet.objects.search_person_by_name("Legitimate").count() == 1
    assert Leaflet.objects.search_person_by_name("Leggy").count() == 0
    # Ensure that we don't fail when we strip all chars from the given name
    assert Leaflet.objects.search_person_by_name("&").count() == 0


def test_manual_updating_search_triggers(db):
    """
    More of a smoke test that these work. The SQL is also run via a migration
    """
    Leaflet.objects.update_name_search()
    Leaflet.objects.update_name_search_trigger()
