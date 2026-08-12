from datetime import timedelta

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

    def test_current_filter(self, all_leaflets):
        today = timezone.localdate()
        current_leaflet = all_leaflets[0]
        current_leaflet.ballots = [
            {"ballot_paper_id": f"test.{today + timedelta(days=1):%Y-%m-%d}"}
        ]
        current_leaflet.save()

        recent_leaflet = all_leaflets[1]
        recent_leaflet.ballots = [
            {"ballot_paper_id": f"test.{today - timedelta(days=20):%Y-%m-%d}"}
        ]
        recent_leaflet.save()

        stale_leaflet = all_leaflets[2]
        stale_leaflet.ballots = [
            {"ballot_paper_id": f"test.{today - timedelta(days=21):%Y-%m-%d}"}
        ]
        stale_leaflet.save()

        assert set(
            LeafletFilter(
                data={"current": "true"}, queryset=Leaflet.objects.all()
            ).qs
        ) == {current_leaflet, recent_leaflet}
        assert set(
            LeafletFilter(
                data={"current": "false"}, queryset=Leaflet.objects.all()
            ).qs
        ) == set(all_leaflets) - {current_leaflet, recent_leaflet}
