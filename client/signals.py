from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile


@receiver(post_save, sender=User)
def create_client_profile(sender, instance, created, **kwargs):
    """Create client profile when user is created via registration"""
    if created:
        # Check if user already has admin profile
        from admin_portal.models import AdminProfile
        if not AdminProfile.objects.filter(user=instance).exists():
            # Create client profile if no admin profile exists
            if not Profile.objects.filter(user=instance).exists():
                Profile.objects.create(user=instance)