from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, BusinessProfile, CustomerProfile, RiderProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 'business':
            BusinessProfile.objects.create(user=instance)
        elif instance.user_type == 'customer':
            CustomerProfile.objects.create(user=instance)
        elif instance.user_type == 'rider':
            RiderProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 'business':
        instance.business_profile.save()
    elif instance.user_type == 'customer':
        instance.customer_profile.save()
    elif instance.user_type == 'rider':
        instance.rider_profile.save() 