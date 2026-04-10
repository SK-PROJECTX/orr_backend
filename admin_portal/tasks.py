"""
Celery tasks for automatic reply system
Handles scheduled and delayed auto-replies
"""

from celery import shared_task
from django.utils import timezone
from datetime import timedelta
import logging

from admin_portal.models import Ticket
from admin_portal.auto_reply_service import AutoReplyService

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def send_delay_notice_task(self, ticket_id, custom_timeframe="48 hours"):
    """
    Celery task to send delay notice after specified time
    """
    try:
        ticket = Ticket.objects.get(id=ticket_id)
        
        # Check if ticket is still active and hasn't been resolved
        if ticket.status not in ['resolved', 'archived']:
            success = AutoReplyService.send_delay_notice(ticket, custom_timeframe)
            
            if success:
                logger.info(f"Delay notice sent for ticket {ticket.ticket_id}")
                return f"Delay notice sent for ticket {ticket.ticket_id}"
            else:
                raise Exception("Failed to send delay notice")
        else:
            logger.info(f"Ticket {ticket.ticket_id} already resolved, skipping delay notice")
            return f"Ticket {ticket.ticket_id} already resolved"
            
    except Ticket.DoesNotExist:
        logger.error(f"Ticket {ticket_id} not found")
        raise Exception(f"Ticket {ticket_id} not found")
    except Exception as exc:
        logger.error(f"Error sending delay notice for ticket {ticket_id}: {exc}")
        # Retry with exponential backoff
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))


@shared_task(bind=True, max_retries=3)
def send_review_message_task(self, ticket_id, custom_timeframe="72 hours"):
    """
    Celery task to send review message after specified time
    """
    try:
        ticket = Ticket.objects.get(id=ticket_id)
        
        # Check if ticket is still active and hasn't been resolved
        if ticket.status not in ['resolved', 'archived']:
            success = AutoReplyService.send_review_message(ticket, custom_timeframe)
            
            if success:
                logger.info(f"Review message sent for ticket {ticket.ticket_id}")
                return f"Review message sent for ticket {ticket.ticket_id}"
            else:
                raise Exception("Failed to send review message")
        else:
            logger.info(f"Ticket {ticket.ticket_id} already resolved, skipping review message")
            return f"Ticket {ticket.ticket_id} already resolved"
            
    except Ticket.DoesNotExist:
        logger.error(f"Ticket {ticket_id} not found")
        raise Exception(f"Ticket {ticket_id} not found")
    except Exception as exc:
        logger.error(f"Error sending review message for ticket {ticket_id}: {exc}")
        # Retry with exponential backoff
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))


@shared_task
def process_contact_message_auto_reply(contact_message_id):
    """
    Celery task to process contact message and send auto-reply
    """
    try:
        from client.models import ContactMessage
        
        contact_message = ContactMessage.objects.get(id=contact_message_id)
        
        # Convert to ticket and send auto-reply
        ticket = AutoReplyService.handle_contact_message_auto_reply(contact_message)
        
        if ticket:
            logger.info(f"Contact message {contact_message_id} converted to ticket {ticket.ticket_id}")
            return f"Contact message converted to ticket {ticket.ticket_id}"
        else:
            raise Exception("Failed to convert contact message to ticket")
            
    except Exception as exc:
        logger.error(f"Error processing contact message {contact_message_id}: {exc}")
        raise exc


@shared_task
def cleanup_old_auto_reply_notifications():
    """
    Periodic task to clean up old auto-reply related notifications
    """
    try:
        from admin_portal.models import SystemNotification
        
        # Delete notifications older than 30 days
        cutoff_date = timezone.now() - timedelta(days=30)
        
        deleted_count = SystemNotification.objects.filter(
            notification_type__in=['ticket_created', 'ticket_assigned'],
            created_at__lt=cutoff_date,
            is_read=True
        ).delete()[0]
        
        logger.info(f"Cleaned up {deleted_count} old auto-reply notifications")
        return f"Cleaned up {deleted_count} notifications"
        
    except Exception as exc:
        logger.error(f"Error cleaning up notifications: {exc}")
        raise exc


@shared_task
def send_admin_whatsapp_notification(ticket_id):
    """
    Celery task to send WhatsApp notification to admin
    This is a placeholder - would integrate with WhatsApp Business API
    """
    try:
        ticket = Ticket.objects.get(id=ticket_id)
        
        # Placeholder for WhatsApp integration
        # In production, this would use WhatsApp Business API
        message = (
            f"🎫 New Client Message\n"
            f"Ticket: {ticket.ticket_id}\n"
            f"Client: {ticket.client.user.get_full_name()}\n"
            f"Subject: {ticket.subject}\n"
            f"Auto-reply sent ✅"
        )
        
        logger.info(f"WhatsApp notification would be sent: {message}")
        
        # In production:
        # whatsapp_client.send_message(
        #     to=settings.ADMIN_WHATSAPP_NUMBER,
        #     message=message
        # )
        
        return f"WhatsApp notification sent for ticket {ticket.ticket_id}"
        
    except Ticket.DoesNotExist:
        logger.error(f"Ticket {ticket_id} not found for WhatsApp notification")
        raise Exception(f"Ticket {ticket_id} not found")
    except Exception as exc:
        logger.error(f"Error sending WhatsApp notification for ticket {ticket_id}: {exc}")
        raise exc



@shared_task(bind=True, max_retries=3)
def check_message_escalation_task(self, ticket_id, last_message_id):
    """
    Check if a ticket needs escalation because no admin has responded.
    """
    try:
        from admin_portal.models import Ticket, TicketMessage
        from admin_portal.email_service import MessageEmailService
        
        ticket = Ticket.objects.get(id=ticket_id)
        
        # If already resolved or escalated elsewhere, skip
        if ticket.status in ['resolved', 'archived'] or ticket.is_escalated:
            return f"Ticket {ticket.ticket_id} is resolved or already escalated"

        # Check for any admin messages since the client message
        has_admin_response = TicketMessage.objects.filter(
            ticket=ticket,
            id__gt=last_message_id,
            sender__is_staff=True
        ).exists()

        if not has_admin_response:
            ticket.is_escalated = True
            ticket.save(update_fields=['is_escalated'])
            
            MessageEmailService.send_escalation_email(ticket)
            logger.info(f"Ticket {ticket.ticket_id} escalated due to inactivity")
            return f"Ticket {ticket.ticket_id} escalated"
        
        return f"Ticket {ticket.ticket_id} has been responded to"

    except Ticket.DoesNotExist:
        logger.error(f"Ticket {ticket_id} not found for escalation check")
        return "Ticket not found"
    except Exception as exc:
        logger.error(f"Error checking escalation for ticket {ticket_id}: {exc}")
        raise self.retry(exc=exc, countdown=300)


# Periodic tasks configuration (would be added to celery beat schedule)
"""
CELERY_BEAT_SCHEDULE = {
    'cleanup-old-notifications': {
        'task': 'admin_portal.tasks.cleanup_old_auto_reply_notifications',
        'schedule': crontab(hour=2, minute=0),  # Run daily at 2 AM
    },
}
"""