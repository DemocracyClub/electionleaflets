from django import template

register = template.Library()

@register.simple_tag
def as_percent(a, b):
    return round(float(a)/float(b)*100, 2)
