from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.conf import settings

User = get_user_model()

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('order', 'Order Update'),
        ('delivery', 'Delivery Update'),
        ('promotion', 'Promotional'),
        ('system', 'System'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.notification_type} - {self.title}"

class NotificationPreferences(models.Model):
    FREQUENCY_CHOICES = (
        ('instant', 'Instant'),
        ('daily', 'Daily Digest'),
        ('weekly', 'Weekly Digest'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    order_updates = models.BooleanField(default=True)
    promotional_updates = models.BooleanField(default=True)
    newsletter = models.BooleanField(default=True)
    quiet_hours_start = models.TimeField(null=True, blank=True)
    quiet_hours_end = models.TimeField(null=True, blank=True)
    notification_frequency = models.CharField(
        max_length=10,
        choices=FREQUENCY_CHOICES,
        default='instant'
    )

    class Meta:
        verbose_name_plural = "Notification preferences"

    def __str__(self):
        return f"Notification preferences for {self.user.username}"

class NotificationTemplate(models.Model):
    TEMPLATE_TYPES = (
        ('email', 'Email'),
        ('push', 'Push Notification'),
        ('sms', 'SMS'),
    )

    name = models.CharField(max_length=100)
    template_type = models.CharField(max_length=10, choices=TEMPLATE_TYPES)
    subject = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.template_type})"

class NotificationLog(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='logs')
    channel = models.CharField(max_length=20, choices=NotificationTemplate.TEMPLATE_TYPES)
    status = models.CharField(max_length=20)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log for {self.notification} via {self.channel}"
