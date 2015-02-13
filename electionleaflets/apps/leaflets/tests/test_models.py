from django.test import TestCase

from leaflets.models import Leaflet, LeafletImage
from .helpers import get_test_image


class LeafletImageTestCase(TestCase):
    def test_raw_image_field(self):
        l = Leaflet()
        l.save()
        image_file = get_test_image()
        li = LeafletImage(image=image_file, leaflet=l)
        self.assertEqual(li.raw_image.name, '')
        li.save()
        self.assertTrue(
            li.raw_image.name.startswith("raw_leaflets/front_test"))
