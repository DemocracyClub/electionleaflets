from django import template
from content.models import ContentBlock

register = template.Library()

@register.inclusion_tag('content/contentblock.html')
def content_block(name):
    try:
        content = ContentBlock.objects.get(name=name).content
    except:
        content = ''
    return { 'content': content }