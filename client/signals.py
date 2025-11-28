from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from notification.utils import notify_user
from .models import ContactMessage, Activity
from scheduling.models import MeetingRequest
User = get_user_model()
from client.tasks.activities import invalidate_recommendations_cache

from .models import Profile

@receiver(post_save, sender=ContactMessage)
def send_contact_notifications(sender, instance, created, **kwargs):
    if not created:
        return

    contact = instance
    admin_users = User.objects.filter(is_staff=True)

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
        contact, 
        "Message Received",
        "We received your message. Our team will contact you soon.",
        ["inapp"], 
       
    )


@receiver(post_save)
def auto_create_activity(sender, instance, created, **kwargs):
    """Auto-create activities for key models"""
    if sender == MeetingRequest and created:
        user = getattr(instance, 'requester', None)
        if not user:
            return
        Activity.objects.create(
                user=user,
                action_type='Meeting Activity',
                title="Upcoming meeting scheduled",
                message="Meeting on {instance.preferred_slots}",
            )
        invalidate_recommendations_cache.delay(user.id)




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