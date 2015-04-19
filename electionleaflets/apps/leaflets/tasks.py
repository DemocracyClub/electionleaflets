from __future__ import absolute_import

from celery import shared_task


@shared_task(name='ocr_leaflet_image')
def ocr_leaflet_image(leaflet_image):
    leaflet_image.ocr()
