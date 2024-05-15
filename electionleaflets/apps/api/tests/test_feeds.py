from django.test import TestCase
from django.urls import reverse
from leaflets.tests.model_factory import LeafletFactory


class TestFeeds(TestCase):
    def setUp(self):
        # make some leaflets
        [LeafletFactory() for i in range(10)]

    def test_latest(self):
        URL = reverse("latest_feed")
        self.client.get(URL)
