from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Trả về giá trị của key trong dictionary."""
    return dictionary.get(str(key), 0)  # Sử dụng .get() cho dictionary