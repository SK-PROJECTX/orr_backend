"""
Automatic Reply Service for Client Tickets
Handles automatic responses to client messages and tickets
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, Optional

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone

from .models import Ticket, TicketMessage, SystemNotification
from client.models import ContactMessage

logger = logging.getLogger(__name__)


class AutoReplyService:
    """Service to handle automatic replies to client messages and tickets"""

    # Default auto-reply templates
    DEFAULT_INITIAL_REPLY = (
        "We acknowledge receipt of your message. Your assigned administrator has been "
        "notified and will follow up with you as soon as practicable via the client portal."
    )

    DEFAULT_DELAY_NOTICE = (
        "Thank you for your message. Your enquiry requires a more detailed review to "
        "ensure an accurate and complete response. I will revert to you within {timeframe}."
    )

    DEFAULT_REVIEW_MESSAGE = (
        "Your message has been reviewed and is currently being assessed. To provide you "
        "with a thorough and accurate response, I will get back to you within {timeframe}. "
        "Thank you for your patience."
    )

    @classmethod
    def send_initial_auto_reply(cls, ticket: Ticket, custom_timeframe: str = "24 hours") -> bool:
        """
        Send initial automatic reply when a ticket is created
        """
        try:
            # Create initial auto-reply message
            initial_message = TicketMessage.objects.create(
                ticket=ticket,
                sender=cls._get_system_user(),
                message=cls.DEFAULT_INITIAL_REPLY,
                is_internal=False  # Visible to client
            )

            # Send notification to admin
            cls._notify_admin_of_new_ticket(ticket)

            logger.info(f"Initial auto-reply sent for ticket {ticket.ticket_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to send initial auto-reply for ticket {ticket.ticket_id}: {e}")
            return False

    @classmethod
    def send_delay_notice(cls, ticket: Ticket, custom_timeframe: str = "48 hours") -> bool:
        """
        Send delay notice if admin is not available for immediate response
        """
        try:
            delay_message = cls.DEFAULT_DELAY_NOTICE.format(timeframe=custom_timeframe)
            
            TicketMessage.objects.create(
                ticket=ticket,
                sender=cls._get_system_user(),
                message=delay_message,
                is_internal=False  # Visible to client
            )

            logger.info(f"Delay notice sent for ticket {ticket.ticket_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to send delay notice for ticket {ticket.ticket_id}: {e}")
            return False

    @classmethod
    def send_review_message(cls, ticket: Ticket, custom_timeframe: str = "72 hours") -> bool:
        """
        Send review message indicating the ticket is being assessed
        """
        try:
            review_message = cls.DEFAULT_REVIEW_MESSAGE.format(timeframe=custom_timeframe)
            
            TicketMessage.objects.create(
                ticket=ticket,
                sender=cls._get_system_user(),
                message=review_message,
                is_internal=False  # Visible to client
            )

            logger.info(f"Review message sent for ticket {ticket.ticket_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to send review message for ticket {ticket.ticket_id}: {e}")
            return False

    @classmethod
    def handle_contact_message_auto_reply(cls, contact_message: ContactMessage) -> Optional[Ticket]:
        """
        Convert ContactMessage to Ticket and send auto-reply
        """
        try:
            # Create ticket from contact message
            ticket = cls._create_ticket_from_contact_message(contact_message)
            
            if ticket:
                # Send initial auto-reply
                cls.send_initial_auto_reply(ticket)
                
                # Mark contact message as processed
                contact_message.is_read = True
                contact_message.save()
                
                logger.info(f"Contact message converted to ticket {ticket.ticket_id} with auto-reply")
                return ticket

        except Exception as e:
            logger.error(f"Failed to handle contact message auto-reply: {e}")
            return None

    @classmethod
    def _create_ticket_from_contact_message(cls, contact_message: ContactMessage) -> Optional[Ticket]:
        """
        Create a ticket from a contact message
        """
        try:
            # Get or create client profile for the user
            from admin_portal.models import Client
            
            client = None
            if contact_message.user:
                try:
                    client = Client.objects.get(user=contact_message.user)
                except Client.DoesNotExist:
                    # Create basic client profile if doesn't exist
                    client = Client.objects.create(
                        user=contact_message.user,
                        company=contact_message.name,  # Use name as company for now
                        primary_pillar="strategic"  # Default pillar
                    )

            if not client:
                logger.warning(f"Cannot create ticket: No client found for contact message {contact_message.id}")
                return None

            # Create ticket
            ticket = Ticket.objects.create(
                client=client,
                subject=f"Client Inquiry from {contact_message.name}",
                description=contact_message.message,
                source="manual_request",
                status="new",
                priority="normal"
            )

            # Generate ticket ID
            ticket.ticket_id = f"TKT-{timezone.now().strftime('%Y%m%d')}-{ticket.pk:03d}"
            ticket.save()

            return ticket

        except Exception as e:
            logger.error(f"Failed to create ticket from contact message: {e}")
            return None

    @classmethod
    def _get_system_user(cls) -> User:
        """
        Get or create system user for auto-replies
        """
        system_user, created = User.objects.get_or_create(
            username="system_auto_reply",
            defaults={
                "first_name": "System",
                "last_name": "Auto Reply",
                "email": "noreply@orr-solutions.com",
                "is_active": True
            }
        )
        return system_user

    @classmethod
    def _notify_admin_of_new_ticket(cls, ticket: Ticket) -> None:
        """
        Notify admin users of new ticket creation
        """
        try:
            # Get admin users who can manage tickets
            admin_users = User.objects.filter(
                admin_profile__role__can_manage_tickets=True,
                admin_profile__is_active=True
            )

            for admin_user in admin_users:
                SystemNotification.objects.create(
                    notification_type="ticket_created",
                    title=f"New Client Message: {ticket.ticket_id}",
                    message=f"New ticket from {ticket.client.user.get_full_name()}: {ticket.subject}",
                    recipient=admin_user,
                    related_ticket=ticket,
                    related_client=ticket.client
                )

        except Exception as e:
            logger.error(f"Failed to notify admin of new ticket: {e}")

    @classmethod
    def schedule_delay_notice(cls, ticket: Ticket, delay_minutes: int = 60, custom_timeframe: str = "48 hours") -> bool:
        """
        Schedule a delay notice to be sent after specified minutes
        """
        try:
            # Import here to avoid circular imports
            from .tasks import send_delay_notice_task, send_admin_whatsapp_notification
            
            # Schedule the delay notice
            send_delay_notice_task.apply_async(
                args=[ticket.id, custom_timeframe],
                countdown=delay_minutes * 60
            )
            
            # Also schedule WhatsApp notification if enabled
            send_admin_whatsapp_notification.apply_async(
                args=[ticket.id],
                countdown=5  # Send WhatsApp notification after 5 seconds
            )
            
            logger.info(f"Delay notice scheduled for ticket {ticket.ticket_id} in {delay_minutes} minutes")
            return True

        except Exception as e:
            logger.error(f"Failed to schedule delay notice: {e}")
            # Fallback to immediate sending if Celery is not available
            return cls.send_delay_notice(ticket, custom_timeframe)