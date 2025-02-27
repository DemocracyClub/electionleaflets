import os
from urllib.parse import urljoin

from django import template
from django.conf import settings
from leaflets.models import Leaflet
from sorl.thumbnail import get_thumbnail

register = template.Library()


@register.inclusion_tag("leaflets/carousel.html")
def leaflet_carousel():
    leaflets = Leaflet.objects.all().order_by("-id")[0:50]
    return {"MEDIA_URL": settings.MEDIA_URL, "leaflets": leaflets}


@register.simple_tag
def get_medium_image_from_upload(file_path):
    path = os.path.join(settings.MEDIA_URL, file_path.name)
    return path.replace("uploads/", "uploads/medium/")


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

    value = str(value)

    if len(value) <= limit:
        return value

    value = value[:limit]
    words = value.split(" ")[:-1]
    return " ".join(words) + "..."


@register.simple_tag(takes_context=True)
def leaflet_og_image_url(context, leaflet):
    if not leaflet.images.exists():
        return None
    leaflet_image = leaflet.images.first()
    return single_image_og_image_url(context, leaflet_image)


@register.simple_tag(takes_context=True)
def single_image_og_image_url(context, leaflet_image):
    request = context["request"]
    full_image_url = request.build_absolute_uri(leaflet_image.image.url)
    thumb_url = get_thumbnail(leaflet_image.image, "600", crop="center").url
    return urljoin(full_image_url, thumb_url)
