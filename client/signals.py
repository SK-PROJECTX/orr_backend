from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from notification.utils import notify_user
from .models import ContactMessage

User = get_user_model()


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
