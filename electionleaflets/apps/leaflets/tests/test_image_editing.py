import os
import shutil
import pytest

from electionleaflets import settings
from leaflets.models import Leaflet, LeafletImage
from .helpers import create_dummy_leaflets


@pytest.fixture
def leaflet_image():
    create_dummy_leaflets()
    return LeafletImage.objects.last()

@pytest.mark.django_db
class TestImageEditing:
    def test_dimensions(self, leaflet_image):
        assert leaflet_image.dimensions == (419, 300)
        
    def test_crop(self, leaflet_image):
        assert leaflet_image.dimensions == (419, 300)
        x = 12
        y = 7
        x2 = 100
        y2 = 100
        leaflet_image.crop(x, y, x2, y2)
        assert leaflet_image.dimensions == (88, 93)
        
    def tearDown(self):
        """
        Remove testing files after tests are run
        """
        # Make sure we're removing the testing dir
        if settings.MEDIA_ROOT.endswith("test_media"):
            for path in ["raw_leaflets", "leaflets"]:
                full_path = os.path.join(settings.MEDIA_ROOT, path)
                if os.path.exists(full_path):
                    shutil.rmtree(full_path)
