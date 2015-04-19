from urllib2 import urlopen
import json

from django.core.management.base import BaseCommand

from constituencies.models import Constituency

class Command(BaseCommand):
    def fetch_constituencies(self):
        base_url = "http://mapit.mysociety.org/"
        req = urlopen(base_url + 'areas/WMC')
        return json.loads(req.read())

    def clean_constituency(self, constituency):
        """
        Takes the raw dict from OpenElectoralCommission and returns a dict
        that's able to be used by the django model.  This is needed because
        this app doesn't support the full JSON provided yet.
        """

        cleaned_constituency = {
            'constituency_id': constituency['id'],
            'name': constituency['name'],
            'country_name': constituency['country_name'],

        }
        return cleaned_constituency


    def handle(self, **options):
        constituencies = self.fetch_constituencies()
        for constituency_id, constituency in constituencies.items():
            print constituency
            Constituency.objects.update_or_create(
                constituency_id=constituency['id'],
                defaults=self.clean_constituency(constituency))
