from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
import threading

from admin_portal.models import AdminProfile, Meeting, Ticket
from notification.utils import notify_user

from .models import Activity

User = get_user_model()
from admin_portal.models import Client
from client.tasks.activities import invalidate_recommendations_cache

from .models import Profile




@receiver(post_save, sender=Ticket)
def notify_admins_on_ticket_created(sender, instance, created, **kwargs):
    if not created or str(instance.ticket_id).startswith('tmp-'):
        return

    ticket = instance

    admin_profiles = AdminProfile.objects.exclude(role__name="content_editor")
    admin_users = [profile.user for profile in admin_profiles if profile.user.is_active]

    for admin in admin_users:
        notify_user(
            admin,
            "New Support Ticket",
            f"New ticket {ticket.ticket_id} created",
            ["inapp", "email"],
            {
                "type": "ticket",
                "template": "support/ticket_created_admin.html",
                "context": {
                    "ticket_id": ticket.ticket_id,
                    "subject": ticket.subject,
                    "priority": ticket.priority,
                    "status": ticket.status,
                    "source": ticket.source,
                    "client_name": (
                        ticket.client.user.first_name
                        if ticket.client and ticket.client.user
                        else ticket.contact_name
                    ),
                    "client_email": (
                        ticket.client.user.email
                        if ticket.client and ticket.client.user
                        else ticket.contact_email
                    ),
                    "description": ticket.description,
                    "created_at": ticket.created_at,
                },
            },
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
    """Create client and profile for new users (only for self-registration)"""
    if created:
        # Skip users who already have an admin profile
        if AdminProfile.objects.filter(user=instance).exists():
            return
            
        # Skip if user is staff or superuser (admin-created)
        if instance.is_staff or instance.is_superuser:
            return
            
        # Skip if this is being created by admin portal (check for specific marker)
        # We'll use a thread-local variable to mark admin-created users
        import threading
        if hasattr(threading.current_thread(), 'skip_auto_client_creation'):
            return

        # Create a general Profile if it doesn't exist
        if not Profile.objects.filter(user=instance).exists():
            Profile.objects.create(user=instance)

        # Create Client if it doesn't exist (only for self-registered users)
        if not Client.objects.filter(user=instance).exists():
            # Provide defaults for required fields
            Client.objects.create(
                user=instance,
                company="N/A",  # or get from registration data
                primary_pillar="strategic",  # default
            )
