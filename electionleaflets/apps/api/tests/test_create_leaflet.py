from django.urls import reverse
from rest_framework.test import APITestCase


class CreateLeafletTests(APITestCase):
    def test_create_leaflet(self):

        leaflet_url = reverse('api:leaflet-list')

        response = self.client.post(leaflet_url, {}, format='json')
        self.assertEqual(response.data['status'], 'draft')
        leaflet_id = response.data['pk']
        self.assertGreater(leaflet_id, 0)
