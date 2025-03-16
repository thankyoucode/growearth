from django import template

register = template.Library()


@register.filter(name="range")
def range_filter(value):
    return range(value)


@register.filter(name="star_range")  # Changed name to avoid conflict
def star_range(value):
    if value is None:
        return []  # Return an empty list if value is None
    try:
        return range(int(value))  # Ensure value is an integer
    except (ValueError, TypeError):
        return []  # Return an empty list if value cannot be converted to an integer


@register.filter(name="split")
def split(value, delimiter):
    """
    Splits the string by the given delimiter.
    """
    return value.split(delimiter)
