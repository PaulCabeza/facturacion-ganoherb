from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def currency(value):
    try:
        decimal_value = Decimal(str(value))
        return "${:.2f}".format(decimal_value)
    except (ValueError, TypeError, decimal.InvalidOperation):
        return "$0.00"

@register.filter
def divide(value, arg):
    try:
        return Decimal(str(value)) / Decimal(str(arg))
    except (ValueError, TypeError, decimal.InvalidOperation, ZeroDivisionError):
        return Decimal('0')

@register.filter
def multiply(value, arg):
    try:
        return Decimal(str(value)) * Decimal(str(arg))
    except (ValueError, TypeError, decimal.InvalidOperation):
        return Decimal('0') 