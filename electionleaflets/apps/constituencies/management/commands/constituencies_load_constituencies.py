import requests
from constituencies.models import Constituency
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def fetch_constituencies(self):
        base_url = "http://mapit.mysociety.org/"
        req = requests.get(base_url + "areas/WMC")
        return req.json()

    def clean_constituency(self, constituency):
        """
        Takes the raw dict from OpenElectoralCommission and returns a dict
        that's able to be used by the django model.  This is needed because
        this app doesn't support the full JSON provided yet.
        """

        return {
            "constituency_id": constituency["id"],
            "name": constituency["name"],
            "country_name": constituency["country_name"],
        }

    def handle(self, **options):
        constituencies = self.fetch_constituencies()
        for constituency_id, constituency in list(constituencies.items()):
            print(constituency)
            Constituency.objects.update_or_create(
                constituency_id=constituency["id"],
                defaults=self.clean_constituency(constituency),
            )
