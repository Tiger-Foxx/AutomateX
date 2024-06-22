from django import template

register = template.Library()

@register.filter(name='index')
def index(sequence, position):
    return sequence[position]

@register.filter(name='range')
def filter_range(value):
    return range(value)