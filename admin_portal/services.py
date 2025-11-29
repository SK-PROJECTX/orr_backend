"""
Admin Portal Services
Provides business logic and external integrations for the admin portal
"""
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from django.contrib.auth.models import User

from .models import (
    Client, Ticket, Meeting, Content, AIConversation, 
    SystemNotification, AuditLog
)

logger = logging.getLogger(__name__)


class NotificationService:
    """Handle email and in-app notifications"""
    
    @staticmethod
    def send_ticket_notification(ticket: Ticket, notification_type: str, recipient: User):
        """Send ticket-related notifications"""
        try:
            # Create in-app notification
            SystemNotification.objects.create(
                notification_type='ticket_assigned' if notification_type == 'assigned' else 'ticket_created',
                title=f'Ticket {ticket.ticket_id} {notification_type}',
                message=f'Ticket: {ticket.subject}',
                recipient=recipient,
                related_ticket=ticket
            )
            
            # Send email if enabled
            if hasattr(settings, 'EMAIL_NOTIFICATIONS_ENABLED') and settings.EMAIL_NOTIFICATIONS_ENABLED:
                subject = f'ORR Admin - Ticket {ticket.ticket_id} {notification_type.title()}'
                message = render_to_string('admin_portal/emails/ticket_notification.html', {
                    'ticket': ticket,
                    'recipient': recipient,
                    'notification_type': notification_type
                })
                
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[recipient.email],
                    html_message=message
                )
                
        except Exception as e:
            logger.error(f"Failed to send ticket notification: {e}")
    
    @staticmethod
    def send_meeting_notification(meeting: Meeting, notification_type: str, recipient: User):
        """Send meeting-related notifications"""
        try:
            # Create in-app notification
            SystemNotification.objects.create(
                notification_type='meeting_updated',
                title=f'Meeting {notification_type}',
                message=f'Meeting with {meeting.client.user.get_full_name()}',
                recipient=recipient,
                related_meeting=meeting
            )
            
            # Send email if enabled
            if hasattr(settings, 'EMAIL_NOTIFICATIONS_ENABLED') and settings.EMAIL_NOTIFICATIONS_ENABLED:
                subject = f'ORR Admin - Meeting {notification_type.title()}'
                message = render_to_string('admin_portal/emails/meeting_notification.html', {
                    'meeting': meeting,
                    'recipient': recipient,
                    'notification_type': notification_type
                })
                
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[recipient.email],
                    html_message=message
                )
                
        except Exception as e:
            logger.error(f"Failed to send meeting notification: {e}")


class AnalyticsService:
    """Advanced analytics calculations"""
    
    @staticmethod
    def calculate_ticket_resolution_time() -> float:
        """Calculate average ticket resolution time in hours"""
        from django.db.models import Avg, F
        
        resolved_tickets = Ticket.objects.filter(
            status='resolved',
            updated_at__isnull=False
        ).annotate(
            resolution_time=F('updated_at') - F('created_at')
        )
        
        if resolved_tickets.exists():
            avg_seconds = resolved_tickets.aggregate(
                avg_time=Avg('resolution_time')
            )['avg_time'].total_seconds()
            return round(avg_seconds / 3600, 2)  # Convert to hours
        
        return 0.0
    
    @staticmethod
    def calculate_meeting_confirmation_time() -> float:
        """Calculate average meeting confirmation time in hours"""
        from django.db.models import Avg, F
        
        confirmed_meetings = Meeting.objects.filter(
            status__in=['confirmed', 'completed'],
            confirmed_datetime__isnull=False
        ).annotate(
            confirmation_time=F('updated_at') - F('created_at')
        )
        
        if confirmed_meetings.exists():
            avg_seconds = confirmed_meetings.aggregate(
                avg_time=Avg('confirmation_time')
            )['avg_time'].total_seconds()
            return round(avg_seconds / 3600, 2)  # Convert to hours
        
        return 0.0
    
    @staticmethod
    def get_client_activity_trends(days: int = 30) -> Dict:
        """Get client activity trends over specified days"""
        end_date = timezone.now()
        start_date = end_date - timedelta(days=days)
        
        # Daily login counts
        daily_logins = []
        for i in range(days):
            date = (end_date - timedelta(days=i)).date()
            count = Client.objects.filter(
                user__last_login__date=date
            ).count()
            daily_logins.append({
                'date': date.isoformat(),
                'count': count
            })
        
        # Stage progression
        stage_changes = AuditLog.objects.filter(
            model_name='Client',
            action='update',
            description__icontains='stage',
            timestamp__gte=start_date
        ).count()
        
        return {
            'daily_logins': daily_logins,
            'stage_changes': stage_changes,
            'period_days': days
        }


class CalendarService:
    """Calendar integration service"""
    
    @staticmethod
    def create_calendar_event(meeting: Meeting) -> Optional[str]:
        """Create calendar event for meeting"""
        # Placeholder for calendar integration
        # In a real implementation, this would integrate with Google Calendar, Outlook, etc.
        try:
            # Generate a mock event ID
            event_id = f"orr_meeting_{meeting.id}_{timezone.now().timestamp()}"
            
            # Log the calendar event creation
            logger.info(f"Calendar event created for meeting {meeting.id}: {event_id}")
            
            return event_id
            
        except Exception as e:
            logger.error(f"Failed to create calendar event: {e}")
            return None
    
    @staticmethod
    def update_calendar_event(meeting: Meeting, event_id: str) -> bool:
        """Update existing calendar event"""
        try:
            # Placeholder for calendar update logic
            logger.info(f"Calendar event updated for meeting {meeting.id}: {event_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update calendar event: {e}")
            return False
    
    @staticmethod
    def delete_calendar_event(event_id: str) -> bool:
        """Delete calendar event"""
        try:
            # Placeholder for calendar deletion logic
            logger.info(f"Calendar event deleted: {event_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete calendar event: {e}")
            return False


class SystemHealthService:
    """Monitor system health and performance"""
    
    @staticmethod
    def get_system_health() -> Dict:
        """Get current system health metrics"""
        try:
            # Database health
            db_health = SystemHealthService._check_database_health()
            
            # Recent errors
            recent_errors = SystemHealthService._get_recent_errors()
            
            # Performance metrics
            performance = SystemHealthService._get_performance_metrics()
            
            return {
                'status': 'healthy' if db_health['status'] == 'ok' else 'warning',
                'database': db_health,
                'recent_errors': recent_errors,
                'performance': performance,
                'last_check': timezone.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"System health check failed: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'last_check': timezone.now().isoformat()
            }
    
    @staticmethod
    def _check_database_health() -> Dict:
        """Check database connectivity and basic metrics"""
        try:
            # Test database connection
            total_clients = Client.objects.count()
            total_tickets = Ticket.objects.count()
            
            return {
                'status': 'ok',
                'total_clients': total_clients,
                'total_tickets': total_tickets,
                'connection': 'healthy'
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'connection': 'failed'
            }
    
    @staticmethod
    def _get_recent_errors(hours: int = 24) -> List[Dict]:
        """Get recent system errors from logs"""
        # In a real implementation, this would read from log files or error tracking service
        return []
    
    @staticmethod
    def _get_performance_metrics() -> Dict:
        """Get basic performance metrics"""
        # Placeholder for performance monitoring
        return {
            'response_time_avg': 150,  # ms
            'memory_usage': 65,  # percentage
            'cpu_usage': 45  # percentage
        }


class ContentService:
    """Content management business logic"""
    
    @staticmethod
    def publish_content(content: Content, user: User) -> bool:
        """Publish content with proper validation and logging"""
        try:
            if content.status == 'published':
                return False
            
            content.status = 'published'
            content.published_at = timezone.now()
            content.save()
            
            # Create audit log
            AuditLog.objects.create(
                user=user,
                action='publish',
                model_name='Content',
                object_id=str(content.id),
                description=f'Published content: {content.title}'
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to publish content {content.id}: {e}")
            return False
    
    @staticmethod
    def archive_content(content: Content, user: User) -> bool:
        """Archive content with proper logging"""
        try:
            content.status = 'archived'
            content.save()
            
            # Create audit log
            AuditLog.objects.create(
                user=user,
                action='archive',
                model_name='Content',
                object_id=str(content.id),
                description=f'Archived content: {content.title}'
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to archive content {content.id}: {e}")
            return False