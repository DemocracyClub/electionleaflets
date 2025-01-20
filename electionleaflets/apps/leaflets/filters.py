import django_filters
from dc_utils.filter_widgets import DSLinkWidget
from django.contrib.humanize.templatetags.humanize import intcomma
from django.db.models import Count
from django.db.models.functions import ExtractYear
from leaflets.models import Leaflet, RegionChoices


def year_facets(queryset=None):
    if not queryset:
        queryset = Leaflet.objects.all()
    return [
        (year, f"{year} ({intcomma(count)})")
        for year, count in queryset.annotate(
            year=ExtractYear("date_uploaded"),
        )
        .values_list("year")
        .annotate(count=Count("id"))
        .distinct()
        .order_by("year")
    ]


def region_facets(queryset=None):
    if not queryset:
        queryset = Leaflet.objects.all()
    choices = []

    ENG_COUNT = 0
    ENG_IDS = [reg.value for reg in RegionChoices.english_regions()]
    qs = (
        queryset.values_list("nuts1")
        .annotate(count=Count("id"))
        .distinct()
        .order_by("nuts1")
    )
    for region, count in qs:
        if not region:
            continue
        choices.append(
            (region, f"{RegionChoices(region).label} ({intcomma(count)})")
        )
        if region in ENG_IDS:
            ENG_COUNT += count

    # Add the 'fake' England filter, but only if no
    # other filter has been applied.
    # If there are no choices, assume England has been selected
    # and add it as a choice
    if ENG_COUNT and (len(choices) > 1 or not choices):
        choices.append(("ENG", f"England ({intcomma(ENG_COUNT)})"))
    return choices


class LeafletFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        choices = year_facets(self.qs)
        self.form.fields["filter_by_year"].choices = choices

        self.form.fields["filter_by_region"].choices = region_facets(self.qs)

    def region_filter(self, queryset, name, value):
        """
        Filter queryset by region using the NUTS1 code
        """
        value = RegionChoices.english_regions() if value == "ENG" else [value]
        return queryset.filter(nuts1__in=value)

    def year_filter(self, queryset, name, value):
        """
        Filter queryset by year of the date uploaded
        """
        return queryset.filter(date_uploaded__year=str(value))

    filter_by_region = django_filters.ChoiceFilter(
        widget=DSLinkWidget(),
        method="region_filter",
        label="Filter by region",
        choices=region_facets,
        empty_label="All regions",
    )

    filter_by_year = django_filters.ChoiceFilter(
        widget=DSLinkWidget(),
        field_name="date_uploaded",
        label="Year uploaded",
        method="year_filter",
        choices=year_facets,
        empty_label="All years",
    )
