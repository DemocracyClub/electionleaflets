import responses

from django.test import TestCase

from leaflets.models import Leaflet, LeafletImage
from .helpers import get_test_image
from .data import MAPIT_POSTCODE_RETURN


class LeafletTestCase(TestCase):
    fixtures = ['constituencies']

    def test_model_initial(self):
        leaflet = Leaflet()
        self.assertEqual(leaflet._initial,
            {'status': None, 'publisher_party': None, 'description': None,
            'title': u'', 'email': u'', 'imprint': None, 'postcode': u'',
            'location': None, 'date_delivered': None, 'reviewed': False,
            'constituency': None, u'id': None, 'name': u''})

        leaflet.status = "draft"
        leaflet.save()
        self.assertNotEqual(leaflet._initial['status'], 'draft')
        leaflet = Leaflet.objects.get(pk=1)
        self.assertEqual(leaflet._initial['status'], 'draft')

    @responses.activate
    def test_leaflet_geocode(self):
        responses.add(
            responses.GET,
            'http://mapit.mysociety.org/postcode/SE228DJ',
             body=MAPIT_POSTCODE_RETURN,
             status=200,
             content_type='application/json',
        )
        l = Leaflet()
        l.geocode('SE228DJ')
        self.assertEqual(l.constituency.name, 'Camberwell and Peckham')
        self.assertEqual(l.location.x, -0.0824797738988752)
        self.assertEqual(l.location.y, 51.4599323104553)

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
