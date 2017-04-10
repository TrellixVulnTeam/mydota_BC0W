from django import template
import datetime

register = template.Library()

@register.filter
def myslugify(value):
    slug = value.replace(" ", "_")
    slug = slug.lower()
    return slug

@register.filter
def fromunix(value):
    return datetime.datetime.fromtimestamp(int(value))