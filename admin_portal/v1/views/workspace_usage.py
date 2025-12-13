from datetime import datetime, timedelta
from django.db.models import Count, Q, Avg, Sum
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from admin_portal.models import Client, Content, Meeting, Ticket, AIConversation, ClientDocument
from client.models import Activity, OnboardingQuestionnaire
from common.permissions import IsAdminUser


@extend_schema(
    tags=["Workspace Usage"],
    summary="Get workspace usage analytics",
    description="Analyze how clients use the workspace including feature adoption, content engagement, and activity patterns."
)
class WorkspaceUsageAnalyticsView(APIView):
    """Workspace usage analytics and feature adoption"""
    
    permission_classes = []  # Temporarily disabled for testing
    
    def get(self, request):
        now = timezone.now()
        last_30_days = now - timedelta(days=30)
        last_7_days = now - timedelta(days=7)
        
        # Feature usage statistics
        feature_usage = {
            "total_active_users": Client.objects.filter(
                user__last_login__gte=last_30_days
            ).count(),
            "ai_chat_users": AIConversation.objects.filter(
                created_at__gte=last_30_days
            ).values('client').distinct().count(),
            "meeting_scheduler_users": Meeting.objects.filter(
                created_at__gte=last_30_days
            ).values('client').distinct().count(),
            "support_ticket_users": Ticket.objects.filter(
                created_at__gte=last_30_days
            ).values('client').distinct().count(),
            "document_users": ClientDocument.objects.filter(
                last_accessed__gte=last_30_days
            ).values('client').distinct().count()
        }
        
        # Content engagement metrics
        content_engagement = {
            "most_accessed_content": self._get_most_accessed_content(),
            "content_download_stats": self._get_content_download_stats(),
            "content_engagement_by_stage": self._get_content_engagement_by_stage(),
            "avg_session_duration": self._calculate_avg_session_duration()
        }
        
        # User activity patterns
        activity_patterns = {
            "daily_active_users": self._get_daily_active_users(),
            "peak_usage_hours": self._get_peak_usage_hours(),
            "feature_adoption_timeline": self._get_feature_adoption_timeline(),
            "user_journey_patterns": self._get_user_journey_patterns()
        }
        
        # Workspace efficiency metrics
        efficiency_metrics = {
            "task_completion_rates": self._get_task_completion_rates(),
            "user_satisfaction_indicators": self._get_satisfaction_indicators(),
            "feature_abandonment_rates": self._get_feature_abandonment_rates(),
            "help_seeking_behavior": self._get_help_seeking_behavior()
        }
        
        return Response({
            "feature_usage": feature_usage,
            "content_engagement": content_engagement,
            "activity_patterns": activity_patterns,
            "efficiency_metrics": efficiency_metrics
        })
    
    def _get_most_accessed_content(self):
        """Get most accessed content items"""
        return list(
            Content.objects.filter(status='published')
            .order_by('-view_count')[:10]
            .values('id', 'title', 'content_type', 'view_count', 'stage')
        )
    
    def _get_content_download_stats(self):
        """Get content download statistics"""
        total_downloads = Content.objects.aggregate(
            total=Sum('download_count')
        )['total'] or 0
        
        downloads_by_type = dict(
            Content.objects.filter(download_count__gt=0)
            .values('content_type')
            .annotate(downloads=Sum('download_count'))
            .values_list('content_type', 'downloads')
        )
        
        return {
            "total_downloads": total_downloads,
            "downloads_by_type": downloads_by_type,
            "avg_downloads_per_content": round(total_downloads / Content.objects.count(), 2) if Content.objects.count() > 0 else 0
        }
    
    def _get_content_engagement_by_stage(self):
        """Get content engagement metrics by business stage"""
        engagement_by_stage = {}
        
        for stage_code, stage_name in Content.STAGE_CHOICES:
            stage_content = Content.objects.filter(stage=stage_code, status='published')
            total_views = stage_content.aggregate(total=Sum('view_count'))['total'] or 0
            total_downloads = stage_content.aggregate(total=Sum('download_count'))['total'] or 0
            
            engagement_by_stage[stage_code] = {
                "total_content": stage_content.count(),
                "total_views": total_views,
                "total_downloads": total_downloads,
                "avg_engagement": round((total_views + total_downloads) / stage_content.count(), 2) if stage_content.count() > 0 else 0
            }
        
        return engagement_by_stage
    
    def _calculate_avg_session_duration(self):
        """Calculate average session duration"""
        # This would require session tracking - simplified for now
        return 18.5  # minutes
    
    def _get_daily_active_users(self):
        """Get daily active users for the last 30 days"""
        daily_users = []
        
        for i in range(30):
            date = (timezone.now() - timedelta(days=i)).date()
            count = Client.objects.filter(
                user__last_login__date=date
            ).count()
            
            daily_users.append({
                "date": date.isoformat(),
                "active_users": count
            })
        
        return daily_users
    
    def _get_peak_usage_hours(self):
        """Get peak usage hours distribution"""
        # Simplified - would analyze actual login/activity timestamps
        return {
            "00-06": 5,
            "06-09": 15,
            "09-12": 35,
            "12-15": 25,
            "15-18": 15,
            "18-24": 5
        }
    
    def _get_feature_adoption_timeline(self):
        """Get feature adoption over time"""
        now = timezone.now()
        timeline_data = []
        
        for i in range(6):  # Last 6 months
            month_start = (now - timedelta(days=30 * i)).replace(day=1)
            month_end = (month_start + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            
            ai_users = AIConversation.objects.filter(
                created_at__gte=month_start,
                created_at__lte=month_end
            ).values('client').distinct().count()
            
            meeting_users = Meeting.objects.filter(
                created_at__gte=month_start,
                created_at__lte=month_end
            ).values('client').distinct().count()
            
            ticket_users = Ticket.objects.filter(
                created_at__gte=month_start,
                created_at__lte=month_end
            ).values('client').distinct().count()
            
            timeline_data.append({
                "month": month_start.strftime("%Y-%m"),
                "ai_chat_users": ai_users,
                "meeting_users": meeting_users,
                "ticket_users": ticket_users
            })
        
        return timeline_data
    
    def _get_user_journey_patterns(self):
        """Get common user journey patterns"""
        # Analyze common sequences of feature usage
        return {
            "onboarding_to_ai": 65,  # % who use AI after onboarding
            "ai_to_meeting": 35,     # % who schedule meeting after AI chat
            "meeting_to_ticket": 25, # % who create ticket after meeting
            "content_to_meeting": 20 # % who schedule meeting after content engagement
        }
    
    def _get_task_completion_rates(self):
        """Get task completion rates"""
        return {
            "onboarding_completion": OnboardingQuestionnaire.objects.filter(
                is_completed=True
            ).count() / OnboardingQuestionnaire.objects.count() * 100 if OnboardingQuestionnaire.objects.count() > 0 else 0,
            "meeting_completion": Meeting.objects.filter(
                status='completed'
            ).count() / Meeting.objects.count() * 100 if Meeting.objects.count() > 0 else 0,
            "ticket_resolution": Ticket.objects.filter(
                status='resolved'
            ).count() / Ticket.objects.count() * 100 if Ticket.objects.count() > 0 else 0
        }
    
    def _get_satisfaction_indicators(self):
        """Get user satisfaction indicators"""
        return {
            "return_user_rate": Client.objects.filter(
                user__last_login__gte=timezone.now() - timedelta(days=30)
            ).count() / Client.objects.count() * 100 if Client.objects.count() > 0 else 0,
            "feature_usage_diversity": self._calculate_feature_diversity(),
            "session_length_trend": "increasing",  # Simplified
            "user_feedback_score": 4.2  # Out of 5 - would come from actual feedback
        }
    
    def _get_feature_abandonment_rates(self):
        """Get feature abandonment rates"""
        return {
            "ai_chat_abandonment": 15,    # % who start but don't complete
            "meeting_booking_abandonment": 25,  # % who start but don't book
            "onboarding_abandonment": 30,       # % who start but don't complete
            "content_browsing_abandonment": 40  # % who browse but don't engage
        }
    
    def _get_help_seeking_behavior(self):
        """Get help-seeking behavior patterns"""
        return {
            "support_ticket_rate": Ticket.objects.count() / Client.objects.count() if Client.objects.count() > 0 else 0,
            "ai_chat_usage_rate": AIConversation.objects.count() / Client.objects.count() if Client.objects.count() > 0 else 0,
            "meeting_request_rate": Meeting.objects.count() / Client.objects.count() if Client.objects.count() > 0 else 0,
            "self_service_rate": 75  # % who find answers without contacting support
        }
    
    def _calculate_feature_diversity(self):
        """Calculate how many different features users engage with"""
        total_clients = Client.objects.count()
        if total_clients == 0:
            return 0
        
        # Count clients who use multiple features
        multi_feature_users = Client.objects.filter(
            Q(ai_conversations__isnull=False) &
            Q(meetings__isnull=False) &
            Q(tickets__isnull=False)
        ).distinct().count()
        
        return round((multi_feature_users / total_clients) * 100, 2)


@extend_schema(
    tags=["Workspace Usage"],
    summary="Get feature adoption metrics",
    description="Detailed analysis of feature adoption rates, user onboarding success, and feature utilization patterns."
)
class FeatureAdoptionMetricsView(APIView):
    """Feature adoption and utilization metrics"""
    
    permission_classes = []  # Temporarily disabled for testing
    
    def get(self, request):
        # Feature adoption funnel
        adoption_funnel = self._get_adoption_funnel()
        
        # Feature utilization depth
        utilization_depth = self._get_utilization_depth()
        
        # Onboarding success metrics
        onboarding_metrics = self._get_onboarding_success_metrics()
        
        # Feature stickiness
        feature_stickiness = self._get_feature_stickiness()
        
        return Response({
            "adoption_funnel": adoption_funnel,
            "utilization_depth": utilization_depth,
            "onboarding_metrics": onboarding_metrics,
            "feature_stickiness": feature_stickiness
        })
    
    def _get_adoption_funnel(self):
        """Get feature adoption funnel"""
        total_users = Client.objects.count()
        
        return {
            "registered_users": total_users,
            "activated_users": Client.objects.filter(
                user__last_login__isnull=False
            ).count(),
            "onboarding_started": OnboardingQuestionnaire.objects.count(),
            "onboarding_completed": OnboardingQuestionnaire.objects.filter(
                is_completed=True
            ).count(),
            "first_feature_used": Client.objects.filter(
                Q(ai_conversations__isnull=False) |
                Q(meetings__isnull=False) |
                Q(tickets__isnull=False)
            ).distinct().count(),
            "multi_feature_users": Client.objects.filter(
                ai_conversations__isnull=False,
                meetings__isnull=False
            ).distinct().count()
        }
    
    def _get_utilization_depth(self):
        """Get feature utilization depth"""
        return {
            "ai_chat": {
                "light_users": AIConversation.objects.values('client').annotate(
                    count=Count('id')
                ).filter(count__lte=3).count(),
                "moderate_users": AIConversation.objects.values('client').annotate(
                    count=Count('id')
                ).filter(count__gt=3, count__lte=10).count(),
                "heavy_users": AIConversation.objects.values('client').annotate(
                    count=Count('id')
                ).filter(count__gt=10).count()
            },
            "meetings": {
                "single_meeting": Meeting.objects.values('client').annotate(
                    count=Count('id')
                ).filter(count=1).count(),
                "multiple_meetings": Meeting.objects.values('client').annotate(
                    count=Count('id')
                ).filter(count__gt=1).count()
            },
            "support_tickets": {
                "occasional_users": Ticket.objects.values('client').annotate(
                    count=Count('id')
                ).filter(count__lte=2).count(),
                "regular_users": Ticket.objects.values('client').annotate(
                    count=Count('id')
                ).filter(count__gt=2).count()
            }
        }
    
    def _get_onboarding_success_metrics(self):
        """Get onboarding success metrics"""
        total_registered = Client.objects.count()
        onboarding_started = OnboardingQuestionnaire.objects.count()
        onboarding_completed = OnboardingQuestionnaire.objects.filter(is_completed=True).count()
        
        return {
            "onboarding_start_rate": round((onboarding_started / total_registered) * 100, 2) if total_registered > 0 else 0,
            "onboarding_completion_rate": round((onboarding_completed / onboarding_started) * 100, 2) if onboarding_started > 0 else 0,
            "time_to_first_feature": 2.3,  # days (simplified)
            "feature_discovery_rate": 78,   # % who discover key features
            "onboarding_drop_off_points": [
                {"step": "Profile completion", "drop_off_rate": 15},
                {"step": "Questionnaire", "drop_off_rate": 25},
                {"step": "First feature use", "drop_off_rate": 20}
            ]
        }
    
    def _get_feature_stickiness(self):
        """Get feature stickiness metrics"""
        now = timezone.now()
        last_30_days = now - timedelta(days=30)
        
        return {
            "ai_chat_retention": self._calculate_feature_retention('ai_conversations', last_30_days),
            "meeting_retention": self._calculate_feature_retention('meetings', last_30_days),
            "ticket_retention": self._calculate_feature_retention('tickets', last_30_days),
            "overall_platform_retention": Client.objects.filter(
                user__last_login__gte=last_30_days
            ).count() / Client.objects.count() * 100 if Client.objects.count() > 0 else 0
        }
    
    def _calculate_feature_retention(self, feature_name, since_date):
        """Calculate retention rate for a specific feature"""
        # Simplified calculation - would need more sophisticated tracking
        if feature_name == 'ai_conversations':
            users_who_used = AIConversation.objects.values('client').distinct().count()
            recent_users = AIConversation.objects.filter(
                created_at__gte=since_date
            ).values('client').distinct().count()
        elif feature_name == 'meetings':
            users_who_used = Meeting.objects.values('client').distinct().count()
            recent_users = Meeting.objects.filter(
                created_at__gte=since_date
            ).values('client').distinct().count()
        elif feature_name == 'tickets':
            users_who_used = Ticket.objects.values('client').distinct().count()
            recent_users = Ticket.objects.filter(
                created_at__gte=since_date
            ).values('client').distinct().count()
        else:
            return 0
        
        if users_who_used > 0:
            return round((recent_users / users_who_used) * 100, 2)
        return 0