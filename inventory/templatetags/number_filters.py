from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def format_decimal(value):
    if value is None:
        return "0.00"
    try:
        # Convertir a Decimal para mayor precisión
        decimal_value = Decimal(str(value))
        # Forzar formato con punto decimal
        return "{:.2f}".format(decimal_value)
    except (ValueError, TypeError, decimal.InvalidOperation):
        return "0.00" 