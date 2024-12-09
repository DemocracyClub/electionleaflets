import pytest
from api.feeds import LatestLeafletsFeed
from leaflets.tests.model_factory import LeafletFactory


@pytest.fixture(autouse=True)
def create_leaflets():
    for _ in range(10):
        LeafletFactory()


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
                description = "{0} – {1}".format(
                    description, item.images.all()[0].image.url
                )
            assert (
                LatestLeafletsFeed.item_description(self, item) == description
            )
