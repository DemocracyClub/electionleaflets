import pytest
from leaflets.models import Leaflet, LeafletImage
from .helpers import get_test_image
from uk_political_parties.models import Party 

@pytest.fixture
def leaflet():
    return Leaflet.objects.create(title="Test Leaflet", description=None)

@pytest.fixture
def party():
    return Party.objects.create(party_name="Labour Party")

@pytest.mark.django_db
def test_model_initial():
    leaflet = Leaflet()
    assert leaflet._initial == {
        'id': None, 'title': '', 'description': None, 'publisher_party': None, 'ynr_party_id': None, 'ynr_party_name': None, 'publisher_person': None, 'ynr_person_id': None, 'ynr_person_name': None, 'ballot_id': None, 'ballots': [], 'people': {}, 'person_ids': [], 'election': None, 'constituency': None, 'imprint': None, 'postcode': '', 'name': '', 'email': '', 'date_delivered': None, 'status': 'draft', 'reviewed': False
    }
    assert leaflet._initial["status"] == "draft"

@pytest.mark.django_db
def test_markdown_error(client, leaflet):
    response = client.get(leaflet.get_absolute_url())
    assert response.status_code == 200

@pytest.mark.django_db
def test_leaflet_detail(client, party):
    leaflet = Leaflet.objects.create(
        title="Test Leaflet", description=None, ynr_party_id="party:1", ynr_party_name="Labour Party", publisher_party=party
    )
    response = client.get(leaflet.get_absolute_url())
    assert response.status_code == 200
    assert "Test Leaflet" in response.content.decode()
    assert "Labour Party" in response.content.decode()

@pytest.mark.django_db
def test_raw_image_field():
    l = Leaflet()
    l.save()
    image_file = get_test_image()
    li = LeafletImage(image=image_file, leaflet=l)
    assert li.raw_image.name == ""
    with open(image_file, "rb") as img_file:
        li.image.save("front_test.jpg", img_file)
    assert "front_test" in li.raw_image.name
