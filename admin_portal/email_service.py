import logging
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)

class MessageEmailService:
    @staticmethod
    def send_admin_new_message_email(ticket, message):
        """
        Notify admin/support staff when a client sends a new message.
        """
        try:
            # Determine recipients
            if ticket.assigned_to:
                recipients = [ticket.assigned_to.email]
            else:
                # Fallback to all admins if unassigned
                recipients = list(User.objects.filter(is_staff=True, is_active=True).values_list('email', flat=True))

            if not recipients:
                logger.warning(f"No recipients found for ticket {ticket.ticket_id}")
                return False

            subject = f"ORR Support: New Message - {ticket.ticket_id}"
            
            # Simple text context for now
            context = {
                'ticket': ticket,
                'message': message,
                'client_name': ticket.client.user.get_full_name(),
                'admin_portal_url': f"https://admin.orr.solutions/tickets/{ticket.id}"
            }
            
            # Use basic formatting if template not found
            try:
                html_message = render_to_string('admin_portal/emails/new_client_message.html', context)
            except Exception:
                html_message = f"""
                <h3>New Client Message</h3>
                <p><b>Ticket:</b> {ticket.ticket_id}</p>
                <p><b>Client:</b> {ticket.client.user.get_full_name()}</p>
                <p><b>Subject:</b> {ticket.subject}</p>
                <p><b>Message:</b></p>
                <p>{message.message}</p>
                <hr>
                <p><a href="{context['admin_portal_url']}">View in Admin Portal</a></p>
                """

            send_mail(
                subject=subject,
                message=message.message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipients,
                html_message=html_message,
                fail_silently=False
            )
            logger.info(f"Admin notification email sent for ticket {ticket.ticket_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to send admin notification email: {e}")
            return False

    @staticmethod
    def send_client_admin_response_email(ticket, message):
        """
        Notify client when an admin responds to their ticket.
        """
        try:
            client = ticket.client
            recipient = client.user.email
            
            if not recipient:
                logger.warning(f"No email for client {client.id}")
                return False

            subject = f"ORR Support Update: Re: {ticket.subject}"
            
            context = {
                'ticket': ticket,
                'message': message,
                'sender_name': message.sender.get_full_name() or "Support Team",
                'client_portal_url': f"https://orr.solutions/messages"
            }

            try:
                html_message = render_to_string('admin_portal/emails/admin_response.html', context)
            except Exception:
                html_message = f"""
                <h3>Support Message Update</h3>
                <p>Hello {client.user.first_name},</p>
                <p>An administrator has responded to your inquiry about "{ticket.subject}".</p>
                <p><b>Latest Message:</b></p>
                <p>{message.message}</p>
                <hr>
                <p><a href="{context['client_portal_url']}">View Message History</a></p>
                """

            send_mail(
                subject=subject,
                message=message.message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient],
                html_message=html_message,
                fail_silently=False
            )
            logger.info(f"Client notification email sent for ticket {ticket.ticket_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to send client notification email: {e}")
            return False

    @staticmethod
    def send_escalation_email(ticket):
        """
        Send escalation email to support management.
        """
        try:
            # For escalation, we send to all staff with management permissions
            recipients = list(User.objects.filter(
                is_staff=True, 
                is_active=True,
                admin_profile__role__can_manage_tickets=True
            ).values_list('email', flat=True))

            if not recipients:
                logger.warning(f"No escalation recipients found")
                return False

            subject = f"⚠️ ESCALATION: Unanswered Ticket {ticket.ticket_id}"
            
            context = {
                'ticket': ticket,
                'admin_portal_url': f"https://admin.orr.solutions/tickets/{ticket.id}"
            }

            html_message = f"""
            <h3>⚠️ Ticket Escalation</h3>
            <p>Ticket <b>{ticket.ticket_id}</b> has remained unanswered for over 4 hours.</p>
            <p><b>Client:</b> {ticket.client.user.get_full_name()}</p>
            <p><b>Subject:</b> {ticket.subject}</p>
            <hr>
            <p><a href="{context['admin_portal_url']}">Review Ticket Immediately</a></p>
            """

            send_mail(
                subject=subject,
                message=f"Ticket {ticket.ticket_id} is escalated due to no response.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipients,
                html_message=html_message,
                fail_silently=False
            )
            logger.info(f"Escalated email sent for ticket {ticket.ticket_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to send escalation email: {e}")
            return False
