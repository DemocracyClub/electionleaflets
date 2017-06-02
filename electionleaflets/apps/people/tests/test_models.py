from django.test import TestCase

import factory
from factory.django import DjangoModelFactory

from uk_political_parties.models import Party
from constituencies.models import Constituency

from elections.models import Election
from people.models import (Person, PartyMemberships,
                           PersonConstituencies)


class YNMPPeopleFactory(DjangoModelFactory):
    class Meta:
        model = Person

    source_name = "YNMP"
    name = factory.Sequence(lambda n: 'user %d' % n)
    remote_id = factory.Sequence(lambda n: '%d' % n)
    source_url = factory.Sequence(lambda n: 'http://yournextmp.com/person/%d/' % n)


class PartyFactory(DjangoModelFactory):
    class Meta:
        model = Party

    party_id = factory.Sequence(lambda n: 'PP%d' % n)
    party_name = factory.Sequence(lambda n: 'Party %d' % n)


class ConstituencyFactory(DjangoModelFactory):
    class Meta:
        model = Constituency

    constituency_id = factory.Sequence(lambda n: str(n))
    name = factory.Sequence(lambda n: 'Constituency %d' % n)


class ElectionFactory(DjangoModelFactory):
    class Meta:
        model = Election

    name = factory.Sequence(lambda n: 'Election %d' % n)
    live_date = "2010-5-6"
    dead_date = "2110-5-6"

# GLOBAL_ELECTION = ElectionFactory(create=False)


class PartyMembershipsFactory(DjangoModelFactory):
    class Meta:
        model = PartyMemberships

    person = factory.SubFactory(YNMPPeopleFactory)
    party = factory.SubFactory(PartyFactory)
    membership_start = "2001-06-7"


class PersonConstituenciesFactory(DjangoModelFactory):
    class Meta:
        model = PersonConstituencies

    person = factory.SubFactory(YNMPPeopleFactory)
    constituency = factory.SubFactory(ConstituencyFactory)
    election = factory.SubFactory(ElectionFactory)


class PersonWithRelations(YNMPPeopleFactory):
    parties = factory.RelatedFactory(PartyMembershipsFactory, 'person')
    constituencies = factory.RelatedFactory(PersonConstituenciesFactory, 'person')

    @factory.post_generation
    def elections(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for election in extracted:
                self.elections.add(election)


class TestModels(TestCase):

    def setUp(self):
        self.person1 = PersonWithRelations()
        self.person1.elections.add(
            self.person1.constituencies.all()[0]
            .personconstituencies_set.all()[0].election
        )

    def test_current_party(self):
        self.assertEqual(self.person1.current_party.pk, 3)

    def test_current_election(self):
        self.assertEqual(self.person1.current_election.pk, 2)

    def test_current_constituency(self):
        self.assertEqual(self.person1.current_constituency.pk, '0')
