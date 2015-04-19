import os

import pytesser

from django.core.management.base import BaseCommand
from django.conf import settings

from leaflets.models import LeafletImage
from leaflets.tasks import ocr_leaflet_image

class Command(BaseCommand):

    def handle(self, **options):
        for leaflet_image in LeafletImage.objects.all().exclude(image="").order_by('-pk'):
            ocr_leaflet_image.delay(leaflet_image)