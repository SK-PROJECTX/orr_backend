import logging
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from admin_portal.models import Ticket

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Check for tickets that have breached SLA and send reminders to admin'

    def add_arguments(self, parser):
        parser.add_argument(
            '--hours',
            type=int,
            default=24,
            help='SLA breach threshold in hours'
        )

    def handle(self, *args, **options):
        hours = options['hours']
        threshold_time = timezone.now() - timedelta(hours=hours)

        # Get tickets that are not resolved and haven't been updated recently
        breaching_tickets = Ticket.objects.filter(
            status__in=['new', 'processing', 'payment_failed', 'payment_disputed', 'refund_requested'],
            updated_at__lt=threshold_time
        ).select_related('assigned_to')

        count = breaching_tickets.count()
        if count == 0:
            self.stdout.write(self.style.SUCCESS('No SLA breaches found.'))
            return

        self.stdout.write(self.style.WARNING(f'Found {count} tickets breaching {hours}h SLA.'))

        for ticket in breaching_tickets:
            admin_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'admin@orr.solutions')
            if ticket.assigned_to and ticket.assigned_to.email:
                admin_email = ticket.assigned_to.email
            else:
                # If you have a specific general admin address, it could go here
                pass

            if not admin_email:
                continue

            subject = f"SLA Breach Alert: Ticket {ticket.ticket_id}"
            message = (
                f"Ticket {ticket.ticket_id} ('{ticket.subject}') has not been updated in over {hours} hours.\n\n"
                f"Current Status: {ticket.status}\n"
                f"Assigned To: {ticket.assigned_to.get_full_name() if ticket.assigned_to else 'Unassigned'}\n\n"
                f"Please review this ticket as soon as possible."
            )

            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@orr.solutions'),
                    recipient_list=[admin_email],
                    fail_silently=True,
                )
                self.stdout.write(self.style.SUCCESS(f'Sent alert for ticket {ticket.ticket_id} to {admin_email}'))
            except Exception as e:
                logger.error(f"Failed to send SLA alert for ticket {ticket.ticket_id}: {e}")

        self.stdout.write(self.style.SUCCESS('SLA check completed.'))
