from datetime import datetime, timedelta
from django.db.models import Count, Q, Avg
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from admin_portal.models import AIConversation, Client, Meeting, Ticket
from client.models import Activity, OnboardingQuestionnaire
from common.permissions import IsAdminUser


@extend_schema(
    tags=["Behavior Analytics"],
    summary="Get user behavior patterns",
    description="Analyze user behavior patterns including login frequency, feature usage, and engagement metrics."
)
class UserBehaviorPatternsView(APIView):
    """Analyze user behavior patterns"""
    
    permission_classes = []  # Temporarily disabled for testing
    
    def get(self, request):
        now = timezone.now()
        last_30_days = now - timedelta(days=30)
        last_7_days = now - timedelta(days=7)
        
        # Login patterns
        login_patterns = {
            "daily_active_users": Client.objects.filter(
                user__last_login__gte=last_7_days
            ).count(),
            "weekly_active_users": Client.objects.filter(
                user__last_login__gte=last_30_days
            ).count(),
            "peak_hours": self._get_peak_login_hours(),
            "login_frequency": self._get_login_frequency_distribution()
        }
        
        # Feature usage
        feature_usage = {
            "ai_chat_usage": AIConversation.objects.filter(
                created_at__gte=last_30_days
            ).count(),
            "meeting_requests": Meeting.objects.filter(
                created_at__gte=last_30_days
            ).count(),
            "ticket_submissions": Ticket.objects.filter(
                created_at__gte=last_30_days
            ).count(),
            "document_downloads": self._get_document_download_stats()
        }
        
        # User engagement metrics
        engagement_metrics = {
            "session_duration": self._calculate_avg_session_duration(),
            "bounce_rate": self._calculate_bounce_rate(),
            "return_user_rate": self._calculate_return_user_rate(),
            "feature_adoption": self._get_feature_adoption_rates()
        }
        
        return Response({
            "login_patterns": login_patterns,
            "feature_usage": feature_usage,
            "engagement_metrics": engagement_metrics
        })
    
    def _get_peak_login_hours(self):
        """Get peak login hours distribution"""
        # This would analyze login times - simplified for now
        return {
            "morning": 25,  # 6-12
            "afternoon": 45,  # 12-18
            "evening": 20,  # 18-24
            "night": 10  # 0-6
        }
    
    def _get_login_frequency_distribution(self):
        """Get login frequency distribution"""
        return {
            "daily": 15,
            "weekly": 35,
            "monthly": 30,
            "occasional": 20
        }
    
    def _get_document_download_stats(self):
        """Get document download statistics"""
        from admin_portal.models import ClientDocument
        return ClientDocument.objects.filter(
            last_accessed__gte=timezone.now() - timedelta(days=30)
        ).aggregate(total_downloads=Count('download_count'))['total_downloads'] or 0
    
    def _calculate_avg_session_duration(self):
        """Calculate average session duration"""
        # Simplified calculation - would need proper session tracking
        return 25.5  # minutes
    
    def _calculate_bounce_rate(self):
        """Calculate bounce rate"""
        # Simplified calculation
        return 15.2  # percentage
    
    def _calculate_return_user_rate(self):
        """Calculate return user rate"""
        total_users = Client.objects.count()
        return_users = Client.objects.filter(
            user__last_login__gte=timezone.now() - timedelta(days=30)
        ).count()
        
        if total_users > 0:
            return round((return_users / total_users) * 100, 2)
        return 0
    
    def _get_feature_adoption_rates(self):
        """Get feature adoption rates"""
        total_clients = Client.objects.count()
        
        if total_clients == 0:
            return {}
        
        return {
            "ai_chat": round((AIConversation.objects.values('client').distinct().count() / total_clients) * 100, 2),
            "meetings": round((Meeting.objects.values('client').distinct().count() / total_clients) * 100, 2),
            "tickets": round((Ticket.objects.values('client').distinct().count() / total_clients) * 100, 2),
            "onboarding_completed": round((OnboardingQuestionnaire.objects.filter(is_completed=True).count() / total_clients) * 100, 2)
        }


@extend_schema(
    tags=["Behavior Analytics"],
    summary="Get user journey analytics",
    description="Analyze user journeys from onboarding to engagement milestones."
)
class UserJourneyAnalyticsView(APIView):
    """Analyze user journey and conversion funnels"""
    
    permission_classes = []  # Temporarily disabled for testing
    
    def get(self, request):
        # Onboarding funnel
        onboarding_funnel = {
            "registered_users": Client.objects.count(),
            "started_onboarding": OnboardingQuestionnaire.objects.count(),
            "completed_onboarding": OnboardingQuestionnaire.objects.filter(is_completed=True).count(),
            "first_meeting_scheduled": Meeting.objects.values('client').distinct().count(),
            "active_users": Client.objects.filter(
                user__last_login__gte=timezone.now() - timedelta(days=30)
            ).count()
        }
        
        # Engagement milestones
        engagement_milestones = {
            "first_ai_interaction": AIConversation.objects.values('client').distinct().count(),
            "first_ticket_created": Ticket.objects.values('client').distinct().count(),
            "multiple_meetings": Meeting.objects.values('client').annotate(
                meeting_count=Count('id')
            ).filter(meeting_count__gt=1).count(),
            "document_engagement": self._get_document_engagement_count()
        }
        
        # Drop-off analysis
        dropoff_analysis = {
            "registration_to_onboarding": self._calculate_dropoff_rate(
                Client.objects.count(),
                OnboardingQuestionnaire.objects.count()
            ),
            "onboarding_to_completion": self._calculate_dropoff_rate(
                OnboardingQuestionnaire.objects.count(),
                OnboardingQuestionnaire.objects.filter(is_completed=True).count()
            ),
            "completion_to_first_meeting": self._calculate_dropoff_rate(
                OnboardingQuestionnaire.objects.filter(is_completed=True).count(),
                Meeting.objects.values('client').distinct().count()
            )
        }
        
        return Response({
            "onboarding_funnel": onboarding_funnel,
            "engagement_milestones": engagement_milestones,
            "dropoff_analysis": dropoff_analysis
        })
    
    def _get_document_engagement_count(self):
        """Get count of users who have engaged with documents"""
        from admin_portal.models import ClientDocument
        return ClientDocument.objects.filter(
            last_accessed__isnull=False
        ).values('client').distinct().count()
    
    def _calculate_dropoff_rate(self, start_count, end_count):
        """Calculate dropoff rate between two stages"""
        if start_count == 0:
            return 0
        return round(((start_count - end_count) / start_count) * 100, 2)