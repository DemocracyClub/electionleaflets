import os
import json

from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

TEST_IMAGES = ['1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg', '1.jpg',]
BASE_PATH = os.path.join(
    os.path.dirname(__file__),
    'test_images'
    )
IMAGES = [(name, os.path.join(BASE_PATH, name)) for name in TEST_IMAGES]

class CreateLeafletTests(APITestCase):
    def test_create_leaflet(self):

        leaflet_url = reverse('api:leaflet-list')
        leaflet_image_url = reverse('api:leafletimage-list')

        response = self.client.post(leaflet_url, {}, format='json')
        self.assertEqual(response.data['status'], 'draft')
        leaflet_id = response.data['pk']
        self.assertGreater(leaflet_id, 0)
