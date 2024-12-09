import pytest
from django.utils import timezone
from leaflets.models import Leaflet

from electionleaflets.apps.api.views import LeafletFilter


@pytest.fixture
def all_leaflets():
    return [
        Leaflet.objects.create(
            title=f"Test Leaflet {i}",
            status="live",
            date_uploaded=timezone.now(),
            modified=timezone.now(),
        )
        for i in range(10)
    ]


@pytest.fixture
def leaflet_with_party(all_leaflets):
    leaflet = all_leaflets[0]
    leaflet.ynr_party_id = "party:1"
    leaflet.ynr_party_name = "Vote for Froglet"
    leaflet.save()
    return leaflet


@pytest.mark.django_db
class TestLeafletFilter:
    def test_ballot_filter(self, all_leaflets):
        leaflet = all_leaflets[0]
        leaflet.ballots = [{"ballot_paper_id": "test"}]
        leaflet.save()
        filter = LeafletFilter(
            data={"ballot": "test"}, queryset=Leaflet.objects.all()
        )
        assert (
            filter.ballot_filter(
                Leaflet.objects.all(), "ballot", "test"
            ).count()
            == 1
        )

    def test_party_filter(self, leaflet_with_party):
        filter = LeafletFilter(
            data={"party": "PP1"}, queryset=Leaflet.objects.all()
        )
        assert (
            filter.party_filter(Leaflet.objects.all(), "party", "PP1").count()
            == 1
        )
