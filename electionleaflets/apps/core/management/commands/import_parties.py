import os
import requests

from django.core.management.base import BaseCommand

from django.conf import settings
from uk_political_parties.models import Party, PartyEmblem


class Command(BaseCommand):
    def clean_party(self, party_id, party):
        cleaned_party = {
            "party_id": party_id,
            "party_name": party["name"],
            "registered_date": party["date_registered"],
            "register": party["register"],
        }
        return cleaned_party

    def handle(self, **options):
        base_url = "https://candidates.democracyclub.org.uk"
        auth_token = getattr(settings, 'YNR_API_KEY')
        params = {"auth_token": auth_token}
        url = "{}/api/next/parties".format(base_url)

        while url:
            req = requests.get(url, params=params)
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
                            party_id=party_id, emblem_url=emblem["image"],
                        )
            url = results.get("next", None)
