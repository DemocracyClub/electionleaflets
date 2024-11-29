from django.core.files import File
from leaflets.models import Leaflet, LeafletImage
from leaflets.tests.conftest import TEST_IMAGE_LOCATION


def create_dummy_leaflets(number=1):
    for i in range(number):
        leaflet = Leaflet()
        leaflet.save()

        li = LeafletImage(leaflet=leaflet)
        li.image.save("test_1.jpg", File(TEST_IMAGE_LOCATION.open("rb")))
        li.save()
