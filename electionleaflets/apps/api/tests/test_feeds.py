import pytest
from django.urls import reverse

from leaflets.tests.model_factory import LeafletFactory

@pytest.fixture
def create_leaflets():
    for _ in range(10):
        LeafletFactory()

@pytest.mark.django_db
def test_latest(client, create_leaflets):
    URL = reverse("latest_feed")
    response = client.get(URL)
    assert response.status_code == 200
