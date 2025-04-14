from django import template

register = template.Library()

@register.filter
def status_color(status):
    color_map = {
        'pending': 'warning',
        'confirmed': 'info',
        'preparing': 'primary',
        'ready': 'success',
        'delivered': 'success',
        'cancelled': 'danger',
    }
    return color_map.get(status.lower(), 'secondary') 