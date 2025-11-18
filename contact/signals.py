import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import ContactMessage
from celery import current_app
logger = logging.getLogger(__name__)  

@receiver(post_save, sender=ContactMessage)
def notify_admin_on_new_contact_message(sender, instance, created, **kwargs):
    """
    When a new ContactMessage is created → send email to all admins
    """
    if not created:
        logger.debug("ContactMessage updated, not created — no admin notification.")
        return 

    logger.info(f"New ContactMessage created (ID={instance.id}). Preparing admin notifications...")

    try:
        admin_emails = list({email for name, email in settings.ADMINS})
    except Exception as e:
        logger.error(f"Failed to load settings.ADMINS: {e}")
        return

    if not admin_emails:
        logger.warning("No admin emails found in settings.ADMINS — skipping notifications.")
        return

    logger.info(f"Admin emails resolved: {admin_emails}")

    subject = f"New Contact Form Submission: {instance.subject}"

    context = {
       "message": {
        "name": instance.first_name,
        "email": instance.email,
        "subject": instance.subject,
        "content": instance.message,
        "created_at": instance.created_at.isoformat(),
    },
        "site_name": "ORR",
    }



    for admin_email in admin_emails:
        logger.info(f"Queueing Celery task for {admin_email}")
        current_app.send_task(
            name="contact.tasks.send_contact_notification_email",  
            args=(subject, admin_email, context),
           
        )



        