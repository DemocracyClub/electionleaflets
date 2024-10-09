from django.test import Client
import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.db import connection

from api.feeds import LatestLeafletsFeed
from leaflets.tests.model_factory import LeafletFactory

@pytest.fixture(autouse=True)
def create_leaflets():
    for _ in range(10):
        LeafletFactory() 

@pytest.fixture
def setup_client():
    client = Client()
    User.objects.create_user(username='testuser', password='12345')
    client.login(username='testuser', password='12345')
    yield client

@pytest.fixture
def teardown_db():
    yield
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM leaflets_leaflet")

@pytest.mark.django_db
class TestLatestLeafletsFeed: 
    def test_items_order(self, create_leaflets):
        create_leaflets  # Access the fixture
        items = LatestLeafletsFeed.items(self)
        ids = [item.id for item in items]
        assert ids == sorted(ids, reverse=True)

    def test_item_title(self, create_leaflets):
        create_leaflets  # Access the fixture
        items = LatestLeafletsFeed.items(self)
        for item in items:
            assert LatestLeafletsFeed.item_title(self, item) == item.get_title()

    def test_item_description(self, create_leaflets):
        create_leaflets  # Access the fixture
        items = LatestLeafletsFeed.items(self)
        for item in items:
            description = ""
            if item.description:
                description = item.description
            if item.images.all():
                description = "{0} – {1}".format(description, item.images.all()[0].image.url)
            assert LatestLeafletsFeed.item_description(self, item) == description
