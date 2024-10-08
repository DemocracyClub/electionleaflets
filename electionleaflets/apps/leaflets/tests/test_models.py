import responses
from unittest import skip
from django.test import TestCase

from leaflets.models import Leaflet, LeafletImage
from .helpers import get_test_image
from .data import MAPIT_POSTCODE_RETURN


class LeafletTestCase(TestCase):
    fixtures = ["constituencies"]

    def test_model_initial(self):
        leaflet = Leaflet()
        self.assertEqual(
            leaflet._initial,
            {'id': None, 'title': '', 'description': None, 'publisher_party': None, 'ynr_party_id': None, 'ynr_party_name': None, 'publisher_person': None, 'ynr_person_id': None, 'ynr_person_name': None, 'ballot_id': None, 'ballots': [], 'people': {}, 'person_ids': [], 'election': None, 'constituency': None, 'imprint': None, 'postcode': '', 'name': '', 'email': '', 'date_delivered': None, 'status': 'draft', 'reviewed': False},
        )

        self.assertEqual(leaflet._initial["status"], "draft")
         
    def test_markdown_error(self):
        leaflet = Leaflet.objects.create(title="Test Leaflet", description=None)
        response = self.client.get(leaflet.get_absolute_url())
        self.assertEqual(response.status_code, 200)

class LeafletImageTestCase(TestCase):
    @skip("fix me after python and django upgrade")
    def test_raw_image_field(self):
        l = Leaflet()
        l.save()
        image_file = get_test_image()
        li = LeafletImage(image=image_file, leaflet=l)
        self.assertEqual(li.raw_image.name, "")
        li.save()
        self.assertRegex(li.raw_image.name, r"front_test")
