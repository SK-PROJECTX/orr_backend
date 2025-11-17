from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from services.email import EmailService  
from .models import ContactMessage

@receiver(post_save, sender=ContactMessage)
def notify_admin_on_new_contact_message(sender, instance, created, **kwargs):
    """
    When a new ContactMessage is created → send email to all admins
    """
    if not created:
        return 
    admin_emails = [email for name, email in settings.admins]  

    if not admin_emails:
        return

    subject = f"New Contact Form Submission: {instance.subject}"

    context = {
        "message": instance,
        "site_name": "ORR",
    }

    email_service = EmailService()

    for admin_email in admin_emails:
        email_service.send_email(
            subject=subject,
            recipient_email=admin_email,
            template_name="contact/contact_admin_notification.html", 
            context=context,
        )