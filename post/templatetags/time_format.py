from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def upto(value, delimiter=None):
    time = value.split(delimiter)[0]
    return f'{time} ago'
upto.is_safe = True
