from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def divide(value, arg):
    try:
        return Decimal(str(value)) / Decimal(str(arg))
    except (ValueError, ZeroDivisionError):
        return value

@register.filter
def multiply(value, arg):
    try:
        return Decimal(str(value)) * Decimal(str(arg))
    except ValueError:
        return value 