from leaflets.filters import LeafletFilter
from leaflets.models import Leaflet, RegionChoices
from leaflets.tests.model_factory import LeafletFactory


def _batch_create_leaflets(count: int, leaflet_attrs: dict):
    for i in range(count):
        LeafletFactory(**leaflet_attrs)


def test_region_filters(db):
    _batch_create_leaflets(10, {"nuts1": RegionChoices.EAST_MIDLANDS.value})
    _batch_create_leaflets(10, {"nuts1": RegionChoices.SCOTLAND.value})
    _batch_create_leaflets(10, {"nuts1": RegionChoices.WALES.value})
    qs = Leaflet.objects.all()

    # Unfiltered
    assert LeafletFilter(queryset=qs).qs.count() == 30

    # Region filter
    assert (
        LeafletFilter(
            data={"filter_by_region": RegionChoices.EAST_MIDLANDS.value},
            queryset=qs,
        ).qs.count()
        == 10
    )


def test_year_filters(db):
    _batch_create_leaflets(10, {"date_uploaded": "2024-01-01"})
    _batch_create_leaflets(10, {"date_uploaded": "2023-01-01"})
    _batch_create_leaflets(10, {"date_uploaded": "2022-01-01"})
    qs = Leaflet.objects.all()

    # Unfiltered
    assert LeafletFilter(queryset=qs).qs.count() == 30

    # Year filter
    assert (
        LeafletFilter(
            data={"filter_by_year": "2024"},
            queryset=qs,
        ).qs.count()
        == 10
    )


def test_combined_filters(db):
    years = ["2024", "2023", "2022"]
    regions = [
        RegionChoices.EAST_MIDLANDS.value,
        RegionChoices.SCOTLAND.value,
        RegionChoices.WALES.value,
    ]
    qs = Leaflet.objects.all()

    for year in years:
        for region in regions:
            _batch_create_leaflets(
                5, {"date_uploaded": f"{year}-01-01", "nuts1": region}
            )
    # Unfiltered
    assert LeafletFilter(queryset=qs).qs.count() == 45

    # One filters at once
    filtered = LeafletFilter(
        data={
            "filter_by_region": RegionChoices.EAST_MIDLANDS.value,
        },
        queryset=qs,
    )

    assert filtered.form.fields["filter_by_year"].choices.choices == [
        (
            2022,
            "2022 (5)",
        ),
        (
            2023,
            "2023 (5)",
        ),
        (
            2024,
            "2024 (5)",
        ),
    ]

    # Two filters at once
    filtered = LeafletFilter(
        data={
            "filter_by_year": "2024",
            "filter_by_region": RegionChoices.EAST_MIDLANDS.value,
        },
        queryset=qs,
    )
    assert filtered.qs.count() == 5

    # Test that the labels are updated and
    # the filters reduce down to one choice
    assert filtered.form.fields["filter_by_year"].choices.choices == [
        (2024, "2024 (5)")
    ]
    assert filtered.form.fields["filter_by_region"].choices.choices == [
        ("UKF", "East Midlands (5)")
    ]
