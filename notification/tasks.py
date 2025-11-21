import logging

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


@shared_task(max_retries=3, default_retry_delay=10)
def send_email_task(subject, recipient_email, template_name, context):
    """
    Send email using Gmail SMTP only
    """
    html_content = render_to_string(template_name, context)

    try:
        send_email_with_gmail(subject, recipient_email, html_content)
        logger.info(f"[Gmail SMTP] Email sent to {recipient_email}")
        return True

    except Exception as e:
        logger.error(f"[Gmail SMTP] Failed: {e}")


def send_email_with_gmail(subject, recipient_email, html_content):
    email = EmailMessage(
        subject=subject,
        body=html_content,
        from_email=settings.EMAIL_HOST_USER,
        to=[recipient_email],
    )
    email.content_subtype = "html"
    email.send()


class EmailService:
    """Handles sending user-related emails (SMTP only)."""

    def __init__(self, default_sender=None):
        self.default_sender = default_sender or settings.DEFAULT_FROM_EMAIL

    def send_email(self, subject, recipient_email, template_name, context):
        try:
            context["from_email"] = "orr.com"

            send_email_task.delay(subject, recipient_email, template_name, context)

            logger.info(f"Email queued for {recipient_email}: {subject}")

        except Exception as e:
            logger.error(f"Failed to queue email to {recipient_email}: {e}")
