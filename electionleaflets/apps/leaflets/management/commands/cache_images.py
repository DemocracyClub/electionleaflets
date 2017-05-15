from django.core.management.base import BaseCommand
from django.conf import settings
from sorl.thumbnail import get_thumbnail
from tqdm import tqdm

from leaflets.models import LeafletImage

class Command(BaseCommand):

    def handle(self, **options):
        for leaflet_image in tqdm(LeafletImage.objects.all().exclude(image="").order_by('?')):
            try:
                get_thumbnail(leaflet_image.image, '350').url
                get_thumbnail(leaflet_image.image, '100x100', crop='center').url
            except:
                pass
