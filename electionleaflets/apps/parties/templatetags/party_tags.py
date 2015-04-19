from django import template
from django.conf import settings
from leaflets.models import Leaflet
from django.db.models import Count

register = template.Library()

@register.inclusion_tag('parties/ordered_list.html')
def party_list_by_count():
    from parties.models import Party
    from datetime import datetime
    when = datetime(year=2010,month=5, day=1)
    parties = Party.objects.order_by('-count').all()[0:10]
    
    return { 'MEDIA_URL': settings.MEDIA_URL, 'parties': parties }