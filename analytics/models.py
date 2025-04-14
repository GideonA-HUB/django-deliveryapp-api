from django.db import models
from accounts.models import BusinessProfile
from orders.models import Order
from services.models import Service
from django.utils.translation import gettext_lazy as _

class BusinessAnalytics(models.Model):
    business = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='analytics')
    date = models.DateField()
    total_orders = models.PositiveIntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    average_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_customers = models.PositiveIntegerField(default=0)
    new_customers = models.PositiveIntegerField(default=0)
    repeat_customers = models.PositiveIntegerField(default=0)
    average_rating = models.FloatField(default=0)
    total_reviews = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('business', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"Analytics for {self.business.business_name} - {self.date}"

class ServiceAnalytics(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='analytics')
    date = models.DateField()
    total_orders = models.PositiveIntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    average_rating = models.FloatField(default=0)
    total_reviews = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('service', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"Analytics for {self.service.name} - {self.date}"

class CustomerAnalytics(models.Model):
    business = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='customer_analytics')
    date = models.DateField()
    total_customers = models.PositiveIntegerField(default=0)
    new_customers = models.PositiveIntegerField(default=0)
    repeat_customers = models.PositiveIntegerField(default=0)
    average_order_frequency = models.FloatField(default=0)
    average_customer_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('business', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"Customer Analytics for {self.business.business_name} - {self.date}"

class DeliveryAnalytics(models.Model):
    business = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='delivery_analytics')
    date = models.DateField()
    total_deliveries = models.PositiveIntegerField(default=0)
    average_delivery_time = models.FloatField(default=0)
    on_time_deliveries = models.PositiveIntegerField(default=0)
    late_deliveries = models.PositiveIntegerField(default=0)
    average_delivery_rating = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('business', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"Delivery Analytics for {self.business.business_name} - {self.date}"

class RevenueAnalytics(models.Model):
    business = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='revenue_analytics')
    date = models.DateField()
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    online_payments = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    cash_payments = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    delivery_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discounts = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    refunds = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('business', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"Revenue Analytics for {self.business.business_name} - {self.date}"
