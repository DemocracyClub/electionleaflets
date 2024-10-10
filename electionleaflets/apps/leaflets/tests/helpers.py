import os

from django.conf import settings
from django.core.files import File

from leaflets.models import Leaflet, LeafletImage


def get_test_image():
    return os.path.join("electionleaflets", "test_media", "test_images", "test_leaflet.jpeg")

def create_dummy_leaflets(number=1):
    for i in range(number):
        l = Leaflet()
        l.save()
        image_file = get_test_image()
        li = LeafletImage(image=image_file, leaflet=l)
        li.image.save("test_1.jpg", File(open(image_file, "rb")))
        li.save()
