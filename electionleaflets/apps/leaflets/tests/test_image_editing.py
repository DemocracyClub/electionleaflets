import shutil
import os

from django.test import TestCase
from django.conf import settings

from leaflets.models import Leaflet, LeafletImage
from .helpers import create_dummy_leaflets

class TestImageCrop(TestCase):
    def setUp(self):
        create_dummy_leaflets()
        self.image_model = LeafletImage.objects.first()

    def test_dimensions(self):
        self.assertEqual(self.image_model.dimensions, (419, 300))

    def test_crop(self):
        self.assertEqual(self.image_model.dimensions, (419, 300))
        x = 12
        y = 7
        x2 = 100
        y2 = 100
        self.image_model.crop(x,y,x2,y2)
        self.assertEqual(self.image_model.dimensions, (88, 93))


    def tearDown(self):
        """
        Remove testing files after tests are run
        """
        #Make sure we're removing the testing dir
        if settings.MEDIA_ROOT.endswith('test_media'):
            for path in ['raw_leaflets', 'leaflets']:
                full_path = os.path.join(settings.MEDIA_ROOT, path)
                if os.path.exists(full_path):
                    shutil.rmtree(full_path)
