from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from orders.models import Order
from accounts.models import RiderProfile, BusinessProfile
from django.utils import timezone

DELIVERY_STATUS_CHOICES = [
    ('PENDING', 'Pending'),
    ('PICKED_UP', 'Picked Up'),
    ('IN_TRANSIT', 'In Transit'),
    ('DELIVERED', 'Delivered'),
    ('CANCELLED', 'Cancelled'),
]

class DeliveryAssignment(models.Model):
    ORDER_STATUS_CHOICES = (
        ('assigned', 'Assigned'),
        ('picked_up', 'Picked Up'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )

    rider = models.ForeignKey('accounts.RiderProfile', on_delete=models.CASCADE, related_name='assignments')
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='delivery_assignments')
    assigned_at = models.DateTimeField(auto_now_add=True)
    picked_up_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='assigned')
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Delivery Assignment for Order {self.order.order_number}"

class DeliveryLocation(models.Model):
    assignment = models.ForeignKey('delivery.DeliveryAssignment', on_delete=models.CASCADE, related_name='locations')
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    speed = models.FloatField(null=True, blank=True)
    accuracy = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Location update for Assignment {self.assignment.id}"

class DeliveryZone(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    city = models.CharField(max_length=100)
    area = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=10, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    businesses = models.ManyToManyField(BusinessProfile, related_name='delivery_zones')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.city}"

class Delivery(models.Model):
    DELIVERY_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('assigned', 'Assigned'),
        ('picked_up', 'Picked Up'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled')
    ]
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='deliveries')
    rider = models.ForeignKey(RiderProfile, on_delete=models.SET_NULL, null=True, related_name='deliveries')
    status = models.CharField(max_length=20, choices=DELIVERY_STATUS_CHOICES, default='pending')
    picked_up_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Delivery {self.id} for Order {self.order.order_number}"

class DeliveryTracking(models.Model):
    delivery = models.ForeignKey('Delivery', on_delete=models.CASCADE, related_name='tracking_points')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=0.0)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=0.0)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=DELIVERY_STATUS_CHOICES)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Tracking for {self.delivery} at {self.timestamp}"

class DeliveryRating(models.Model):
    delivery = models.OneToOneField(Delivery, on_delete=models.CASCADE, related_name='rating', null=True, blank=True)
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Rating for Delivery {self.delivery.id if self.delivery else 'N/A'}: {self.rating}/5"

class ZoneBoundary(models.Model):
    zone = models.ForeignKey('delivery.DeliveryZone', on_delete=models.CASCADE, related_name='boundaries')
    latitude = models.FloatField()
    longitude = models.FloatField()
    order = models.IntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Boundary point for {self.zone.name}"

class DeliveryFee(models.Model):
    zone = models.ForeignKey('delivery.DeliveryZone', on_delete=models.CASCADE, related_name='fees')
    min_distance = models.FloatField(help_text='Minimum distance in kilometers')
    max_distance = models.FloatField(help_text='Maximum distance in kilometers')
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Delivery fee for {self.zone.name} ({self.min_distance}km - {self.max_distance}km)"
