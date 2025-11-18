import logging
from celery import shared_task
from common.tasks import EmailService
from celery import current_app
logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def send_contact_notification_email(self, subject, recipient, context):
    """
    Task to send admin notification emails asynchronously.
    """
    try:
        logger.info(f"[ContactTask] Sending contact notification to {recipient}")
        current_app.send_task(
            "common.tasks.send_email_task",
            args=(subject, recipient, "contact/contact_admin_notification.html", context)
        )
        logger.info(f"[ContactTask] Email successfully queued by EmailService for {recipient}")
        return True

    except Exception as e:
        logger.error(f"[ContactTask] FAILED for {recipient}: {e}")
        return False
