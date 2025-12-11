import logging
import sib_api_v3_sdk
from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from sib_api_v3_sdk.rest import ApiException

logger = logging.getLogger(__name__)


@shared_task(max_retries=3, default_retry_delay=10)
def send_email_task(subject, recipient_email, template_name, context):
    """
    Try Brevo API → fallback to SMTP.
    """
    html_content = render_to_string(template_name, context)

    try:
        send_via_api(subject, recipient_email, html_content)
        logger.info(f"[Brevo API] Email sent → {recipient_email}")
        return True

    except Exception as api_error:
        logger.error(f"[Brevo API] Failed → {api_error}")


    try:
        send_via_smtp(subject, recipient_email, html_content)
        logger.info(f"[SMTP Fallback] Email sent → {recipient_email}")
        return True

    except Exception as smtp_error:
        logger.error(f"[SMTP Fallback] Failed → {smtp_error}")
        raise smtp_error  


def send_via_api(subject, recipient_email, html_content):
    """Brevo API sending"""
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key["api-key"] = settings.BREVO_API_KEY

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )

    email_request = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": recipient_email}],
        subject=subject,
        html_content=html_content,
        sender={"name": "Orr", "email": settings.DEFAULT_FROM_EMAIL},
    )

    response = api_instance.send_transac_email(email_request)
    return response


def send_via_smtp(subject, recipient_email, html_content):
    """SMTP fallback using Django EmailBackend"""
    msg = EmailMultiAlternatives(
        subject=subject,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[recipient_email]
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return True


class EmailService:
    """Public interface"""
    def __init__(self, default_sender=None):
        self.default_sender = default_sender or settings.DEFAULT_FROM_EMAIL

    def send_email(self, subject, recipient_email, template_name, context):
        context["from_email"] = self.default_sender

        send_email_task.delay(subject, recipient_email, template_name, context)
        logger.info(f"[EmailService] Queued → {recipient_email}")

        return True
