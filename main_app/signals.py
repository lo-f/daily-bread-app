from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_or_save_user_profile(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        
        if not hasattr(instance, 'profile'):
            Profile.objects.create(
                user=instance,
                name='', 
                age=0,
                height=0.0,
                weight=0.0,
            )