from constituencies.models import Constituency
from django import template
from django.conf import settings

register = template.Library()


@register.inclusion_tag("constituencies/ordered_list.html")
def constituency_list_by_count():
    constituencies = Constituency.objects.all().order_by("-count")[0:10]
    return {"MEDIA_URL": settings.MEDIA_URL, "constituencies": constituencies}


@register.inclusion_tag("constituencies/zero_entry_list.html")
def constituency_list_with_none():
    constituencies = Constituency.objects.filter(count=0).all()[0:10]
    return {"MEDIA_URL": settings.MEDIA_URL, "constituencies": constituencies}
