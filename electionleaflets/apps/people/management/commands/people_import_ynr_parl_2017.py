import csv
import datetime

import requests

from django.core.management.base import BaseCommand

from elections.models import Election
from constituencies.models import Constituency
from uk_political_parties.models import Party
from people.models import Person, PartyMemberships, PersonConstituencies

SOURCE = "YNR2017"


class Command(BaseCommand):

    def handle(self, **options):
        base_url = "https://candidates.democracyclub.org.uk"
        csv_url = "{}/media/candidates-parl.2017-06-08.csv".format(base_url)
        req = requests.get(csv_url, verify=False)
        req.encoding = 'utf-8'
        csv_data = csv.DictReader(req.text.splitlines())

        # Source is always the 2017 General Election
        election, _ = Election.objects.update_or_create(
            name="UK General election 2017",
            live_date="2017-04-18",
            dead_date="2017-06-30",
        )

        for line in csv_data:
            defaults = {
                'name': line['name']
            }

            person, created = Person.objects.update_or_create(
                remote_id=line['id'],
                source_name=SOURCE,
                source_url="{0}/person/{1}".format(
                    base_url,
                    line['id']),
                defaults=defaults
            )

            parties = Party.objects.filter(party_name=line['party_name'])
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

            constituency = Constituency.objects.get(
                name=line['post_label'])
            PersonConstituencies.objects.update_or_create(
                person=person,
                constituency=constituency,
                election=election
            )
