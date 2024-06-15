# testing/templatetags/custom_tags.py
from django import template

register = template.Library()

@register.simple_tag
def range_tag(value):
    return range(int(value))

@register.filter
def add_one(value):
    return value + 1