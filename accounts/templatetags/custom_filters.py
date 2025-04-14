from django import template

register = template.Library()

@register.filter
def get_status_color(status):
    status_colors = {
        'pending': 'warning',
        'confirmed': 'info',
        'preparing': 'primary',
        'ready': 'success',
        'assigned': 'info',
        'picked_up': 'primary',
        'in_transit': 'info',
        'delivered': 'success',
        'cancelled': 'danger',
    }
    return status_colors.get(status, 'secondary') 