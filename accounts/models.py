from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('customer', 'Customer'),
        ('business', 'Business'),
        ('rider', 'Rider'),
    )
    
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='customer')
    phone_number = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

class BusinessProfile(models.Model):
    BUSINESS_TYPE_CHOICES = (
        ('restaurant', 'Restaurant'),
        ('grocery', 'Grocery Store'),
        ('pharmacy', 'Pharmacy'),
        ('retail', 'Retail Store'),
        ('other', 'Other'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='business_profile')
    business_name = models.CharField(max_length=100)
    business_type = models.CharField(max_length=20, choices=BUSINESS_TYPE_CHOICES)
    business_logo = models.ImageField(upload_to='business_logos/', blank=True, null=True)
    description = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.business_name

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()}'s Profile"

class CustomerAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    address_name = models.CharField(max_length=50, help_text="e.g., Home, Office")
    street_address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = _('Customer Addresses')
        ordering = ['-is_default', '-created_at']

    def __str__(self):
        return f"{self.address_name} - {self.street_address}"

    def save(self, *args, **kwargs):
        if self.is_default:
            # Set all other addresses of this customer as non-default
            CustomerAddress.objects.filter(customer=self.customer).exclude(id=self.id).update(is_default=False)
        super().save(*args, **kwargs)

class RiderProfile(models.Model):
    VEHICLE_TYPE_CHOICES = (
        ('bicycle', 'Bicycle'),
        ('motorcycle', 'Motorcycle'),
        ('car', 'Car'),
        ('scooter', 'Scooter'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='rider_profile')
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPE_CHOICES)
    license_number = models.CharField(max_length=50, blank=True)
    is_available = models.BooleanField(default=True)
    current_location_lat = models.FloatField(null=True, blank=True)
    current_location_lng = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()}'s Rider Profile"
