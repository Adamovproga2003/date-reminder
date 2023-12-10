from django import template

register = template.Library()


@register.filter
def get_last_digit(value):
    return str(value)[-1]
