import csv
import io
import datetime

import requests

from django.core.management.base import BaseCommand

from elections.models import Election
from constituencies.models import Constituency
from uk_political_parties.models import Party
from people.models import Person, PartyMemberships, PersonConstituencies

SOURCE = "YNMP2015"


class Command(BaseCommand):

    def handle(self, **options):
        csv_url = "https://yournextmp.com/media/candidates.csv"
        req = requests.get(csv_url, verify=False)
        content = io.StringIO(req.content)
        csv_data = csv.DictReader(content)

        # Source is always the 2015 General Election
        election = Election.objects.get(name="UK General election 2015")

        for line in csv_data:
            defaults = {
                'name': line['name']
            }

            person, created = Person.objects.update_or_create(
                remote_id=line['id'],
                source_name=SOURCE,
                source_url="https://yournextmp.com/person/{0}".format(
                    line['id']),
                defaults=defaults
            )

            if created:
                parties = Party.objects.filter(party_name=line['party'])
                if parties:
                    party = parties[0]
                    PartyMemberships.objects.update_or_create(
                        person=person,
                        party=party,
                        defaults={
                            'membership_start': datetime.datetime.now()
                        }
                    )
                person.elections.add(election)

                constituency = Constituency.objects.get(pk=line['mapit_id'])
                PersonConstituencies.objects.update_or_create(
                    person=person,
                    constituency=constituency,
                    election=election
                )
