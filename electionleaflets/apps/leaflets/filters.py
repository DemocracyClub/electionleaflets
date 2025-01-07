import django_filters
from dc_utils.filter_widgets import DSLinkWidget
from leaflets.models import RegionChoices


class LeafletFilter(django_filters.FilterSet):
    def region_filter(self, queryset, name, value):
        """
        Filter queryset by region using the NUTS1 code
        """
        value = RegionChoices.english_regions() if value == "ENG" else [value]
        return queryset.filter(nuts1__in=value)

    filter_by_region = django_filters.ChoiceFilter(
        widget=DSLinkWidget(),
        method="region_filter",
        label="Filter by region",
        choices=RegionChoices.choices + [("ENG", "England")],
    )
