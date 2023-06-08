from django import template

from collections import Counter

register = template.Library()


@register.filter
def replace(value):
    return value.replace("-", " ")


@register.filter
def _rating(value):
    value = int(value)
    if value not in [1, 2, 3, 4, 5]:
        value = 0
    x = []
    for i in range(value):
        x += ['fa fa-star']
    for i in range(5 - value):
        x += ['fa fa-star-o']
    return x


@register.filter
def colors(value):
    colors = Counter()
    for i in value:
        colors[i.color] += 1
    return [(color, count) for color, count in colors.items()]
