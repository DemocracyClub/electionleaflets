import django_filters
from dc_utils.filter_widgets import DSLinkWidget


def region_choices():
    """
    Return a list of tuples with NUTS1 code and label. Used by the region filter
    on the BaseBallotFilter
    """
    return [
        ("UKC", "North East"),
        ("UKD", "North West"),
        ("UKE", "Yorkshire and the Humber"),
        ("UKF", "East Midlands"),
        ("UKG", "West Midlands"),
        ("UKH", "East of England"),
        ("UKI", "London"),
        ("UKJ", "South East"),
        ("UKK", "South West"),
        ("UKL", "Wales"),
        ("UKM", "Scotland"),
        ("UKN", "Northern Ireland"),
    ]


class LeafletFilter(django_filters.FilterSet):
    def region_filter(self, queryset, name, value):
        """
        Filter queryset by region using the NUTS1 code
        """
        return queryset.filter(nuts1=value)

    filter_by_region = django_filters.ChoiceFilter(
        widget=DSLinkWidget(),
        method="region_filter",
        label="Filter by region",
        choices=region_choices,
    )
