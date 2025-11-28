from datetime import datetime, timedelta
from django.db.models import Count, Q
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from common.permissions import IsAdminUser
from drf_spectacular.utils import extend_schema

from admin_portal.models import Client, Ticket, Meeting, SystemNotification, AIConversation
from ..serializers.dashboard import (
    DashboardStatsSerializer, QuickClientSerializer, 
    QuickTicketSerializer, QuickMeetingSerializer
)


@extend_schema(
    tags=["Admin Dashboard"],
    summary="Get dashboard overview metrics",
    description="Retrieve key metrics for the admin dashboard including active clients, pending tickets, upcoming meetings, system notifications, portal logins, AI chat sessions, and escalation rates."
)
class DashboardOverviewView(APIView):
    """Admin dashboard overview with key metrics"""
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        # Calculate date ranges
        now = timezone.now()
        seven_days_ago = now - timedelta(days=7)
        
        # Active clients (logged in within last 30 days)
        active_clients = Client.objects.filter(
            user__last_login__gte=now - timedelta(days=30)
        ).count()
        
        # Pending tickets by status
        pending_tickets = {
            'new': Ticket.objects.filter(status='new').count(),
            'in_progress': Ticket.objects.filter(status='in_progress').count(),
            'waiting_client': Ticket.objects.filter(status='waiting_client').count(),
        }
        
        # Upcoming meetings (next 7 days)
        upcoming_meetings = Meeting.objects.filter(
            confirmed_datetime__gte=now,
            confirmed_datetime__lte=now + timedelta(days=7),
            status='confirmed'
        ).count()
        
        # System notifications (unread)
        system_notifications = SystemNotification.objects.filter(
            recipient=request.user,
            is_read=False
        ).count()
        
        # Portal logins in last 7 days
        portal_logins_7days = Client.objects.filter(
            user__last_login__gte=seven_days_ago
        ).count()
        
        # AI chat sessions and escalation rate
        ai_sessions = AIConversation.objects.filter(
            created_at__gte=seven_days_ago
        ).count()
        
        escalated_sessions = AIConversation.objects.filter(
            created_at__gte=seven_days_ago,
            escalated_to_ticket=True
        ).count()
        
        escalation_rate = (escalated_sessions / ai_sessions * 100) if ai_sessions > 0 else 0
        
        stats_data = {
            'active_clients': active_clients,
            'pending_tickets': pending_tickets,
            'upcoming_meetings': upcoming_meetings,
            'system_notifications': system_notifications,
            'portal_logins_7days': portal_logins_7days,
            'ai_chat_sessions': ai_sessions,
            'escalation_rate': round(escalation_rate, 2)
        }
        
        serializer = DashboardStatsSerializer(stats_data)
        return Response(serializer.data)


@extend_schema(
    tags=["Admin Dashboard"],
    summary="Get recent activity feed",
    description="Retrieve recent activity including the latest clients, tickets, and meetings for the dashboard feed."
)
class RecentActivityView(APIView):
    """Recent activity feed for dashboard"""
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        # Recent clients (last 10)
        recent_clients = Client.objects.select_related('user').order_by('-created_at')[:10]
        
        # Recent tickets (last 10)
        recent_tickets = Ticket.objects.select_related('client__user').order_by('-created_at')[:10]
        
        # Recent meetings (last 10)
        recent_meetings = Meeting.objects.select_related('client__user').order_by('-created_at')[:10]
        
        return Response({
            'recent_clients': QuickClientSerializer(recent_clients, many=True).data,
            'recent_tickets': QuickTicketSerializer(recent_tickets, many=True).data,
            'recent_meetings': QuickMeetingSerializer(recent_meetings, many=True).data,
        })


@extend_schema(
    tags=["Admin Dashboard"],
    summary="Get quick statistics",
    description="Retrieve quick statistics for dashboard widgets including today's metrics and weekly summaries."
)
class QuickStatsView(APIView):
    """Quick statistics for dashboard widgets"""
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        now = timezone.now()
        
        # Today's stats
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        
        return Response({
            'today': {
                'new_tickets': Ticket.objects.filter(created_at__gte=today_start).count(),
                'meetings_scheduled': Meeting.objects.filter(
                    confirmed_datetime__date=now.date(),
                    status='confirmed'
                ).count(),
                'ai_conversations': AIConversation.objects.filter(
                    created_at__gte=today_start
                ).count(),
            },
            'this_week': {
                'tickets_resolved': Ticket.objects.filter(
                    status='resolved',
                    updated_at__gte=now - timedelta(days=7)
                ).count(),
                'meetings_completed': Meeting.objects.filter(
                    status='completed',
                    updated_at__gte=now - timedelta(days=7)
                ).count(),
                'new_clients': Client.objects.filter(
                    created_at__gte=now - timedelta(days=7)
                ).count(),
            }
        })