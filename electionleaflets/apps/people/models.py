from django.db import models

from constituencies.models import Constituency
from uk_political_parties.models import Party
from elections.models import Election



class Person(models.Model):
    name = models.CharField(blank=False, max_length=255)
    remote_id = models.CharField(blank=True, max_length=255, null=True)
    source_url = models.URLField(blank=True, null=True)
    source_name = models.CharField(blank=True, max_length=100)
    image_url = models.URLField(blank=True, null=True)
    elections = models.ManyToManyField(Election)
    parties = models.ManyToManyField(Party, through='PartyMemberships')
    constituencies = models.ManyToManyField(Constituency, through='PersonConstituencies')


    @property
    def current_party(self):
        parties = self.partymemberships_set.filter(membership_end=None)
        if parties:
            return parties[0]

    @property
    def current_election(self):
        return self.elections.filter(active=True)[0]

    @property
    def current_constituency(self):
        return self.constituencies.filter(
            personconstituencies__election=self.current_election)[0]

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.remote_id)


class PartyMemberships(models.Model):
    person = models.ForeignKey(Person)
    party = models.ForeignKey(Party)
    membership_start = models.DateField()
    membership_end = models.DateField(null=True)


class PersonConstituencies(models.Model):
    person = models.ForeignKey(Person)
    constituency = models.ForeignKey(Constituency)
    election = models.ForeignKey(Election)
