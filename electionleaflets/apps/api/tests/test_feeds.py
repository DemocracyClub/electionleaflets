import pytest
from django.contrib.auth.models import User

from api.feeds import ConstituencyFeed, LatestLeafletsFeed
from constituencies.models import Constituency
from leaflets.tests.model_factory import LeafletFactory

@pytest.fixture(autouse=True)
def create_leaflets():
    for _ in range(10):
        LeafletFactory()

@pytest.fixture
def create_constituency():
    return Constituency.objects.create(name="test_name", slug="test_slug")

@pytest.mark.django_db
class TestLatestLeafletsFeed:
    def test_items_order(self, create_leaflets):
        items = LatestLeafletsFeed.items(self)
        ids = [item.id for item in items]
        assert ids == sorted(ids, reverse=True)

    def test_item_title(self, create_leaflets):
        items = LatestLeafletsFeed.items(self)
        for item in items:
            assert LatestLeafletsFeed.item_title(self, item) == item.get_title()

    def test_item_description(self, create_leaflets):
        items = LatestLeafletsFeed.items(self)
        for item in items:
            description = ""
            if item.description:
                description = item.description
            if item.images.all():
                description = "{0} – {1}".format(description, item.images.all()[0].image.url)
            assert LatestLeafletsFeed.item_description(self, item) == description

@pytest.mark.django_db
class TestConstituencyFeed:
    def test_get_object(self, create_constituency):
        feed = ConstituencyFeed()
        obj = feed.get_object(None, create_constituency.slug)
        assert obj.slug == create_constituency.slug
        assert feed.link == "/constituencies/%s/" % obj.slug
        assert feed.description == "The most recently uploaded leaflets for %s" % obj.name

    def test_items(self, create_leaflets, create_constituency):
        LeafletFactory(constituency=create_constituency)
        feed = ConstituencyFeed()
        items = feed.items(create_constituency)
        assert items.count() == 1

    def test_item_title(self, create_constituency):
        feed = ConstituencyFeed()
        item = LeafletFactory()
        assert feed.item_title(item) == item.title

    def test_item_description(self, create_constituency):
        feed = ConstituencyFeed()
        item = LeafletFactory()
        assert feed.item_description(item) == item.description
