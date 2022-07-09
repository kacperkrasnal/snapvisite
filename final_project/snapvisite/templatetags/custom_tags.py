from django import template
from snapvisite.models import Company, Category

register = template.Library()


@register.simple_tag
def all_categories():
    return Category.objects.all()


@register.filter(name='times')
def times(number):
    return range(number)


@register.simple_tag
def define(val=None):
  return val


@register.filter('duration_format')
def duration_format(value):
    hours = int(value/60)
    minutes = value % 60

    if hours == 0:
        return f'{minutes}min'
    else:
        if minutes == 0:
            return f'{hours}h'
        else:
            return f'{hours}h{minutes}min'


