from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def upto(value, delimiter=None):
    time = value.split(delimiter)[0]
    return f'{time} ago'.upper()
upto.is_safe = True


@register.filter
@stringfilter
def shortUpto(value, delimiter=None):
    time = value.split(delimiter)[0].split('\xa0')
    return f'{time[0]}{time[1][0]}'

upto.is_safe = True
shortUpto.is_safe = True
