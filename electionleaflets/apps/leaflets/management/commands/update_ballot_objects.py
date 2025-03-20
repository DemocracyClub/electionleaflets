"""
This command will iterate over all leaflets and update the ballot object.

This is useful if the object shape changes over time, or if we want to add
more keys to it from YNR

"""

from core.helpers import YNRAPIHelper
from django.core.management.base import BaseCommand
from leaflets.models import Leaflet


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.ballot_cache = {}
        self.ynr_api = YNRAPIHelper()
        for leaflet in Leaflet.objects.all():
            self.update_leaflet_ballots(leaflet)

    def update_leaflet_ballots(self, leaflet: Leaflet):
        if not leaflet.ballots:
            return

        new_ballot_data = []
        for ballot in leaflet.ballots:
            ballot_id = ballot["ballot_paper_id"]
            ballot_data = self.get_ballot_data(ballot_id)

            ballot["election_id"] = ballot_data["election"]["election_id"]
            ballot["election_name"] = ballot_data["election"]["name"]
            ballot["ballot_title"] = (
                f"{ballot_data['election']['name']}: {ballot_data['post']['label']}"
            )
            new_ballot_data.append(ballot)
        leaflet.ballots = [
            dict(t) for t in {tuple(d.items()) for d in new_ballot_data}
        ]
        leaflet.save()
        self.stdout.write(
            f"Updated {leaflet} with {[leaflet['ballot_paper_id'] for leaflet in leaflet.ballots]}"
        )

    def get_ballot_data(self, ballot_paper_id):
        if ballot_paper_id not in self.ballot_cache:
            ynr_ballot_data = self.ynr_api.get(
                f"ballots/{ballot_paper_id}",
            )
            self.ballot_cache[ballot_paper_id] = ynr_ballot_data

        return self.ballot_cache[ballot_paper_id]
