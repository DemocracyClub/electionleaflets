import requests
from django.core.management.base import BaseCommand
from uk_political_parties.models import Party, PartyEmblem


class Command(BaseCommand):
    def clean_party(self, party_id, party):
        return {
            "party_id": party_id,
            "party_name": party["name"],
            "registered_date": party["date_registered"],
            "register": party["register"],
        }

    def handle(self, **options):
        base_url = "https://candidates.democracyclub.org.uk"
        url = "{}/api/next/parties/".format(base_url)

        while url:
            req = requests.get(url)
            results = req.json()
            organizations = results["results"]
            for org in organizations:
                party_id = org["ec_id"]
                print(party_id, org["name"])
                (party_obj, created) = Party.objects.update_or_create(
                    party_id=party_id, defaults=self.clean_party(party_id, org)
                )

                if org["emblems"]:
                    for emblem in org["emblems"]:
                        PartyEmblem.objects.update_or_create(
                            party_id=party_id,
                            emblem_url=emblem["image"],
                        )
            url = results.get("next", None)
