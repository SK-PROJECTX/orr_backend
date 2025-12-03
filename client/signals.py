from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from admin_portal.models import AdminProfile, Meeting
from notification.utils import notify_user

from .models import Activity, ContactMessage

User = get_user_model()
from admin_portal.models import Client
from client.tasks.activities import invalidate_recommendations_cache

from .models import Profile


@receiver(post_save, sender=ContactMessage)
def send_contact_notifications(sender, instance, created, **kwargs):
    if not created:
        return

    contact = instance
    admin_profiles = AdminProfile.objects.exclude(role__name="content_editor")
    admin_users = [profile.user for profile in admin_profiles]

    for admin in admin_users:
        notify_user(
            admin,
            "New Support Message",
            f"You received a support message from {contact.name}",
            ["inapp", "email"],
            {
                "type": "contact",
                "template": "support/support_message_admin.html",
                "context": {
                    "name": contact.name,
                    "email": contact.email,
                    "website": contact.website,
                    "message": contact.message,
                    "submitted_at": contact.created_at,
                },
            },
        )
    notify_user(
        contact.user,
        "Message Received",
        "We received your message. Our team will contact you soon.",
        ["inapp"],
    )


@receiver(post_save)
def auto_create_activity(sender, instance, created, **kwargs):
    """Auto-create activities for key models"""
    if sender == Meeting and created:
        user = getattr(instance, "requester", None)
        if not user:
            return
        Activity.objects.create(
            user=user,
            action_type="Meeting Activity",
            title="Upcoming meeting scheduled",
            message="Meeting on {instance.requested_datetime}",
        )
        invalidate_recommendations_cache.delay(user.id)


@receiver(post_save, sender=User)
def create_profiles(sender, instance, created, **kwargs):
    """Create client and profile for new users"""
    if created:
        # Skip users who already have an admin profile
        if not AdminProfile.objects.filter(user=instance).exists():

            # Create a general Profile if it doesn't exist
            if not Profile.objects.filter(user=instance).exists():
                Profile.objects.create(user=instance)

            # Create Client if it doesn't exist
            if not Client.objects.filter(user=instance).exists():
                # Provide defaults for required fields
                Client.objects.create(
                    user=instance,
                    company="N/A",  # or get from registration data
                    primary_pillar="strategic",  # default
                )
