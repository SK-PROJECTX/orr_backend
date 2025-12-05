import logging
import sib_api_v3_sdk
from celery import shared_task
from django.conf import settings
from django.template.loader import render_to_string
from sib_api_v3_sdk.rest import ApiException
logger = logging.getLogger(__name__)


@shared_task(max_retries=3, default_retry_delay=10)
def send_email_task(subject, recipient_email, template_name, context):
    """
    Send email using Brevo SMTP .
    """
    html_content = render_to_string(template_name, context)

    try:
        send_smtp_email(subject, recipient_email, html_content)
        logger.info(f"[Brevo SMTP] Email sent to {recipient_email}")
        return True

    except Exception as e:
        logger.error(f"[Brevo SMTP] Failed to send email to {recipient_email}: {e}")
        raise  


def send_smtp_email(subject, recipient_email, html_content):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key["api-key"] = settings.BREVO_API_KEY

  
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )

    send_smtp_email_request = sib_api_v3_sdk.SendSmtpEmail( 
        to=[{"email": recipient_email}],
        subject=subject,
        html_content=html_content,
        sender={"name": "Orr", "email": settings.DEFAULT_FROM_EMAIL},
        headers={"charset": "utf-8"}
    )

    try:
        response = api_instance.send_transac_email(send_smtp_email_request)
        return response

    except ApiException as e:
        error_msg = f"Brevo API error: {e.status} - {e.body if hasattr(e, 'body') else str(e)}"
        logger.error(error_msg)
        raise Exception(error_msg)


class EmailService:
    """Handles sending user-related emails (Brevo SMTP only)."""

    def __init__(self, default_sender=None):
        self.default_sender = default_sender or settings.DEFAULT_FROM_EMAIL

    def send_email(self, subject, recipient_email, template_name, context):
        try:
            context["from_email"] = "info@orr.solutions"


            send_email_task.delay(subject, recipient_email, template_name, context)

            logger.info(f"Email queued for {recipient_email}: {subject}")
            return True  

        except Exception as e:
            logger.error(f"Failed to queue email to {recipient_email}: {e}")
            raise  