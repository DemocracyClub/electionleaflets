import os
import re
import csv
import datetime

from django.core.management.base import BaseCommand
from django.conf import settings

from analysis.models import LeafletProperties
from constituencies.models import Constituency
from uk_political_parties.models import Party
from leaflets.models import Leaflet

class Command(BaseCommand):
    YES_VALUES = [
        re.compile('^yes.*'),
        re.compile('.*front of a leaflet.*'),
    ]

    NO_VALUES = [re.compile('^no'), re.compile('^on')]
    NA_VALUES = [
        re.compile('^too poor quality'), re.compile('^n/a'),
        re.compile('^na'), re.compile('^\?')]
    NA_VALUES = [
        re.compile('^too poor quality'), re.compile('^n/a'),
        re.compile('^na'), re.compile('^\?'),
    ]
    LEAFLET_VALUES = [re.compile('.*leaflet.*'), re.compile('^leaflets$')]
    CV_VALUES = [re.compile('^cv$')]
    LETTER_VALUES = [re.compile('^letter.*'), re.compile('^leter.*'),
        re.compile('^personal letter$')]
    MAGAZINE_VALUES = [re.compile('^magazine.*')]
    NEWSLETTER_VALUES = [re.compile('^newsletter.*'),
        re.compile('.*newletter.*'), re.compile('^newsleter.*'),
        re.compile('^local newsletter.*')]
    NEWSPAPER_VALUES = [re.compile('^newspaper.*'),
        re.compile('^newpaper.*')]
    SURVEY_VALUES = [re.compile('^survey.*'),
        re.compile('^newpaper.*')]


    def _is_match(self, value, match_list):
       return set([
           x.match(value) for x in match_list if x.match(value)
       ])

    def clean_value(self, value):
        value = value.lower().strip()
        if self._is_match(value, self.YES_VALUES):
            return "Yes"
        if self._is_match(value, self.NO_VALUES):
            return "No"
        if self._is_match(value, self.NA_VALUES):
            return "n/a"

        return value

    def clean_style_value(self, value):
        value = value.lower().strip()
        if self._is_match(value, self.CV_VALUES):
            return 'CV'
        if self._is_match(value, self.LETTER_VALUES):
            return 'Letter'
        if self._is_match(value, self.MAGAZINE_VALUES):
            return 'Magazine'
        if self._is_match(value, self.NEWSLETTER_VALUES):
            return 'Newsletter'
        if self._is_match(value, self.NA_VALUES) or\
             self._is_match(value, self.NO_VALUES):
            return "n/a"
        if self._is_match(value, self.NEWSPAPER_VALUES):
            return 'Newspaper'
        if self._is_match(value, self.SURVEY_VALUES):
            return 'Survey'
        if self._is_match(value, self.LEAFLET_VALUES):
            return 'Leaflet'
        return "--%s" % value

    def handle(self, **options):
        csv_path = os.path.join(
            os.path.abspath(settings.PROJECT_ROOT),
            'apps/analysis/legacy_data.csv'
        )
        for line in csv.DictReader(open(csv_path)):
            leaflet_id = line['Leaflet Link'].strip('/').split('/')[-1].strip()
            if not leaflet_id:
                continue
            leaflets = Leaflet.objects.filter(pk=leaflet_id)

            if not leaflets:
                continue
            leaflet = leaflets[0]

            def _add_question(question, answer):
                question, created = LeafletProperties.objects.update_or_create(
                    leaflet=leaflet,
                    user_id=2,
                    key=question,
                    defaults={
                        'value': answer
                    }
                )


            if self.clean_value(line['Leader mentioned']):
                _add_question('has_leader', self.clean_value(line['Leader mentioned']))

            if self.clean_style_value(line['Leaflet Style (Leaflet, Letter, Magazine, Newsletter, Newspaper, CV or Survey)']):
                _add_question('leaflet_style', self.clean_style_value(line['Leaflet Style (Leaflet, Letter, Magazine, Newsletter, Newspaper, CV or Survey)']))

            if self.clean_value(line['Leader Picture included']):
                _add_question('has_leader_photo', self.clean_value(line['Leader Picture included']))

            if self.clean_value(line['Party Logo']):
                _add_question('has_logo', self.clean_value(line['Party Logo']))

            if self.clean_value(line['Opposition leader pictured']):
                _add_question('has_opposition_leader_photo', self.clean_value(line['Opposition leader pictured']))

            if self.clean_value(line['Opposition leader mentioned']):
                _add_question('has_opposition_leader', self.clean_value(line['Opposition leader mentioned']))

            if self.clean_value(line['Does it include a graph?']):
                _add_question('include_graph', self.clean_value(line['Does it include a graph?']))

            if self.clean_value(line["""squeeze message"""]):
                _add_question('squeeze_message', self.clean_value(line["""squeeze message"""]))






