from django.db import models
from accounts.models import User
from services.models import Service
from django.utils.translation import gettext_lazy as _

class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferences')
    preferred_categories = models.ManyToManyField('services.Category', blank=True)
    preferred_price_range_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    preferred_price_range_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    preferred_rating_min = models.FloatField(null=True, blank=True)
    preferred_delivery_time_max = models.PositiveIntegerField(null=True, blank=True, help_text='Maximum delivery time in minutes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Preferences for {self.user.get_full_name()}"

class UserBehavior(models.Model):
    BEHAVIOR_TYPES = (
        ('view', 'View'),
        ('search', 'Search'),
        ('add_to_cart', 'Add to Cart'),
        ('purchase', 'Purchase'),
        ('review', 'Review'),
        ('rating', 'Rating'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='behaviors')
    behavior_type = models.CharField(max_length=20, choices=BEHAVIOR_TYPES)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='user_behaviors')
    timestamp = models.DateTimeField(auto_now_add=True)
    data = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.behavior_type} - {self.service.name}"

class ServiceRecommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='recommendations')
    score = models.FloatField()
    reason = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        ordering = ['-score']
        unique_together = ('user', 'service')

    def __str__(self):
        return f"Recommendation for {self.user.get_full_name()} - {self.service.name}"

class PopularService(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='popularity')
    view_count = models.PositiveIntegerField(default=0)
    purchase_count = models.PositiveIntegerField(default=0)
    average_rating = models.FloatField(default=0)
    total_ratings = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-purchase_count']

    def __str__(self):
        return f"Popularity stats for {self.service.name}"

class TrendingService(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='trending')
    period = models.CharField(max_length=20)  # e.g., 'daily', 'weekly', 'monthly'
    score = models.FloatField()
    rank = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['period', 'rank']
        unique_together = ('service', 'period')

    def __str__(self):
        return f"Trending {self.period} - {self.service.name}"

class SimilarService(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='similar_services')
    similar_to = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='similar_from')
    similarity_score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-similarity_score']
        unique_together = ('service', 'similar_to')

    def __str__(self):
        return f"{self.service.name} similar to {self.similar_to.name}"
