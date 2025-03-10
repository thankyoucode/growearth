from django import template

register = template.Library()


@register.filter(name="multiply")  # Use @register.filter for filters
def multiply(value, arg):
    """Multiplies two numbers."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def format_float(value, decimal_places=2):
    """Formats a float to the specified number of decimal places."""
    try:
        return f"{float(value):.{decimal_places}f}"
    except (ValueError, TypeError):
        return value
