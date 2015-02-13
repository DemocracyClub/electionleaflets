import os

from django.conf import settings
from django.core.files import File

from leaflets.models import Leaflet, LeafletImage

def create_dummy_leaflets(number=1):
    for i in range(number):
        l = Leaflet()
        l.save()
        image_file = os.path.join(
            settings.MEDIA_ROOT,'test_images/front_test.jpg')
        li = LeafletImage(image=image_file, leaflet=l)
        li.image.save('test_1.jpg', File(open(image_file, 'r')))
        li.save()