import logging

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def send_contact_notification_email(self, subject, recipient, context):
    """
    Task to send admin notification emails asynchronously.
    """
    from notification.tasks import send_email_task

    try:
        logger.info(f"[ContactTask] Sending contact notification to {recipient}")
        send_email_task(
            subject, recipient, "contact/contact_admin_notification.html", context
        )
        return True

    except Exception as e:
        logger.error(f"[ContactTask] FAILED for {recipient}: {e}")
        return False
