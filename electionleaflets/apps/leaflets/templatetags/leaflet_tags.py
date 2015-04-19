from django import template
from django.conf import settings
from leaflets.models import Leaflet
import os

register = template.Library()

@register.inclusion_tag('leaflets/carousel.html')
def leaflet_carousel():
    leaflets = Leaflet.objects.all().order_by('-id')[0:50]
    return { 'MEDIA_URL': settings.MEDIA_URL, 'leaflets': leaflets }

@register.simple_tag
def get_medium_image_from_upload(file_path):
    path = os.path.join(settings.MEDIA_URL, file_path.name)
    path = path.replace('uploads/', 'uploads/medium/')
    return path

@register.filter
def truncatesmart(value, limit=80):
    """
    Truncates a string after a given number of chars keeping whole words.

    Usage:
        {{ string|truncatesmart }}
        {{ string|truncatesmart:50 }}
    """
    try:
        limit = int(limit)
    except ValueError:
        return value

    value = unicode(value)

    if len(value) <= limit:
        return value

    value = value[:limit]
    words = value.split(' ')[:-1]
    return ' '.join(words) + '...'