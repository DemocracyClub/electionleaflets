from django import template
from django.conf import settings
from categories.models import Category

register = template.Library()


@register.inclusion_tag('categories/ordered_list.html')
def category_list():
    return {'MEDIA_URL': settings.MEDIA_URL, 'categories': Category.objects.order_by('name').all()}
