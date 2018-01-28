from django import template

register = template.Library()


@register.simple_tag
def as_percent(a, b):
    if not a:
        return 0
    if not b:
        return 0
    return round(float(a) / float(b) * 100, 2)
