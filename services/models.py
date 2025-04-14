from django.db import models
from accounts.models import BusinessProfile, CustomerProfile
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = _('categories')
        ordering = ['name']

    def __str__(self):
        return self.name

class Service(models.Model):
    business = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='services')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='service_images/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    preparation_time = models.PositiveIntegerField(help_text='Preparation time in minutes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.business.business_name}"

class ServiceOption(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='options')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.service.name}"

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    services = models.ManyToManyField(Service, related_name='tags', blank=True)

    def __str__(self):
        return self.name

class BusinessLocation(models.Model):
    business = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='locations')
    address = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.business.business_name} - {self.address}"

class BusinessSchedule(models.Model):
    DAY_CHOICES = (
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    )

    business = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='schedule')
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    is_closed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('business', 'day')

    def __str__(self):
        return f"{self.business.business_name} - {self.day}"

class ServiceRating(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='ratings')
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('service', 'customer')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.customer.user.get_full_name()} rated {self.service.name} {self.rating}/5"

class ServiceAvailability(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='availability')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    available_slots = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('service', 'date', 'start_time')
        ordering = ['date', 'start_time']

    def __str__(self):
        return f"{self.service.name} - {self.date} {self.start_time}-{self.end_time}"
