from django import template
from django.db.models import F, Q

register = template.Library()


@register.filter(name='subtract')
def subtract(value, arg):
    return value - arg


@register.filter
def filter_not_purchased_gifts(value, gift):
    result = gift.filter(~Q(bought_quantity=F('quantity')))
    return result


@register.filter
def filter_purchased_gifts(value, gift):
    result = gift.filter(~Q(bought_quantity=0))
    return result
