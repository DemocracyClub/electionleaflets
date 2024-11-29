import pytest
from constituencies.models import Constituency
from elections.models import Election
from people.models import PartyMemberships, Person, PersonConstituencies
from uk_political_parties.models import Party


@pytest.fixture
def person():
    return Person.objects.create(name="John Doe")

@pytest.fixture
def party():
    return Party.objects.create(party_name="Test Party")

@pytest.fixture
def constituency():
    return Constituency.objects.create(name="Test Constituency")

@pytest.fixture
def election():
    return Election.objects.create(name="Test Election", live_date="2023-01-01", dead_date="2023-01-01")


@pytest.mark.django_db
def test_create_party_membership(person, party):
    membership = PartyMemberships.objects.create(person=person, party=party, membership_start="2023-01-01")
    assert membership.person == person
    assert membership.party == party
    assert membership.membership_start == "2023-01-01"
    assert membership.membership_end is None

@pytest.mark.django_db
def test_create_person_constituency(person, constituency, election):
    person_constituency = PersonConstituencies.objects.create(person=person, constituency=constituency, election=election)
    assert person_constituency.person == person
    assert person_constituency.constituency == constituency
    assert person_constituency.election == election

@pytest.mark.django_db
def test_person_current_party(person, party):
    PartyMemberships.objects.create(person=person, party=party, membership_start="2023-01-01")
    assert person.current_party.party == party

@pytest.mark.django_db
def test_person_current_election(person, election):
    person.elections.add(election)
    assert person.current_election == election

@pytest.mark.django_db
def test_person_current_constituency(person, constituency, election):
    PersonConstituencies.objects.create(person=person, constituency=constituency, election=election)
    person.elections.add(election)
    assert person.current_constituency == constituency

@pytest.mark.django_db
def test_person_unicode(person):
    assert str(person.name) == "John Doe"