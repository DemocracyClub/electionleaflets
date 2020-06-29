from django import template
from django.conf import settings

register = template.Library()


@register.inclusion_tag("parties/ordered_list.html")
def party_list_by_count():
    from parties.models import Party

    parties = Party.objects.order_by("-count").all()[0:10]

    return {"MEDIA_URL": settings.MEDIA_URL, "parties": parties}
