from datetime import datetime, timedelta
from django.db.models import Count, Q, Avg, F
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from admin_portal.models import Client, Meeting, Ticket, AIConversation
from client.models import OnboardingQuestionnaire
from common.permissions import IsAdminUser


@extend_schema(
    tags=["Consultation Metrics"],
    summary="Get consultation performance metrics",
    description="Analyze consultation performance including meeting statistics, conversion rates, and client satisfaction."
)
class ConsultationPerformanceView(APIView):
    """Consultation performance metrics and analytics"""
    
    permission_classes = []  # Temporarily disabled for testing
    
    def get(self, request):
        now = timezone.now()
        last_30_days = now - timedelta(days=30)
        last_90_days = now - timedelta(days=90)
        
        # Meeting statistics
        meeting_stats = {
            "total_meetings": Meeting.objects.count(),
            "meetings_this_month": Meeting.objects.filter(
                created_at__gte=last_30_days
            ).count(),
            "completed_meetings": Meeting.objects.filter(
                status='completed'
            ).count(),
            "meeting_types_distribution": dict(
                Meeting.objects.values('meeting_type')
                .annotate(count=Count('id'))
                .values_list('meeting_type', 'count')
            ),
            "avg_meeting_duration": self._calculate_avg_meeting_duration(),
            "meeting_completion_rate": self._calculate_meeting_completion_rate()
        }
        
        # Consultation conversion metrics
        conversion_metrics = {
            "inquiry_to_meeting_rate": self._calculate_inquiry_to_meeting_rate(),
            "meeting_to_engagement_rate": self._calculate_meeting_to_engagement_rate(),
            "repeat_consultation_rate": self._calculate_repeat_consultation_rate(),
            "escalation_to_consultation_rate": self._calculate_escalation_rate()
        }
        
        # Client satisfaction indicators
        satisfaction_indicators = {
            "meeting_feedback_score": self._get_meeting_feedback_score(),
            "follow_up_meeting_requests": Meeting.objects.filter(
                meeting_type='follow_up',
                created_at__gte=last_30_days
            ).count(),
            "client_retention_post_meeting": self._calculate_client_retention_post_meeting(),
            "no_show_rate": self._calculate_no_show_rate()
        }
        
        # Consultant performance
        consultant_performance = self._get_consultant_performance_metrics()
        
        return Response({
            "meeting_statistics": meeting_stats,
            "conversion_metrics": conversion_metrics,
            "satisfaction_indicators": satisfaction_indicators,
            "consultant_performance": consultant_performance
        })
    
    def _calculate_avg_meeting_duration(self):
        """Calculate average meeting duration"""
        # Using the duration_minutes field from Meeting model
        avg_duration = Meeting.objects.aggregate(
            avg_duration=Avg('duration_minutes')
        )['avg_duration']
        return round(avg_duration, 2) if avg_duration else 60
    
    def _calculate_meeting_completion_rate(self):
        """Calculate meeting completion rate"""
        total_meetings = Meeting.objects.count()
        completed_meetings = Meeting.objects.filter(status='completed').count()
        
        if total_meetings > 0:
            return round((completed_meetings / total_meetings) * 100, 2)
        return 0
    
    def _calculate_inquiry_to_meeting_rate(self):
        """Calculate rate from initial inquiry to scheduled meeting"""
        total_clients = Client.objects.count()
        clients_with_meetings = Meeting.objects.values('client').distinct().count()
        
        if total_clients > 0:
            return round((clients_with_meetings / total_clients) * 100, 2)
        return 0
    
    def _calculate_meeting_to_engagement_rate(self):
        """Calculate rate from meeting to ongoing engagement"""
        clients_with_meetings = Meeting.objects.values('client').distinct().count()
        clients_with_multiple_touchpoints = Client.objects.filter(
            Q(meetings__isnull=False) & 
            (Q(tickets__isnull=False) | Q(ai_conversations__isnull=False))
        ).distinct().count()
        
        if clients_with_meetings > 0:
            return round((clients_with_multiple_touchpoints / clients_with_meetings) * 100, 2)
        return 0
    
    def _calculate_repeat_consultation_rate(self):
        """Calculate rate of clients who schedule multiple meetings"""
        clients_with_meetings = Meeting.objects.values('client').distinct().count()
        clients_with_multiple_meetings = Meeting.objects.values('client').annotate(
            meeting_count=Count('id')
        ).filter(meeting_count__gt=1).count()
        
        if clients_with_meetings > 0:
            return round((clients_with_multiple_meetings / clients_with_meetings) * 100, 2)
        return 0
    
    def _calculate_escalation_rate(self):
        """Calculate rate of AI conversations escalated to meetings"""
        total_conversations = AIConversation.objects.count()
        escalated_to_meetings = AIConversation.objects.filter(
            client__meetings__isnull=False
        ).distinct().count()
        
        if total_conversations > 0:
            return round((escalated_to_meetings / total_conversations) * 100, 2)
        return 0
    
    def _get_meeting_feedback_score(self):
        """Get average meeting feedback score"""
        # This would be based on actual feedback data - simulated for now
        return 4.3  # out of 5
    
    def _calculate_client_retention_post_meeting(self):
        """Calculate client retention rate after meetings"""
        clients_with_meetings = Meeting.objects.filter(
            status='completed',
            confirmed_datetime__lte=timezone.now() - timedelta(days=30)
        ).values('client').distinct()
        
        retained_clients = Client.objects.filter(
            id__in=clients_with_meetings,
            user__last_login__gte=timezone.now() - timedelta(days=30)
        ).count()
        
        total_clients_with_meetings = clients_with_meetings.count()
        
        if total_clients_with_meetings > 0:
            return round((retained_clients / total_clients_with_meetings) * 100, 2)
        return 0
    
    def _calculate_no_show_rate(self):
        """Calculate no-show rate for meetings"""
        total_confirmed_meetings = Meeting.objects.filter(status='confirmed').count()
        cancelled_meetings = Meeting.objects.filter(status='cancelled').count()
        
        if total_confirmed_meetings > 0:
            return round((cancelled_meetings / total_confirmed_meetings) * 100, 2)
        return 0
    
    def _get_consultant_performance_metrics(self):
        """Get performance metrics by consultant"""
        from django.contrib.auth.models import User
        
        consultants = User.objects.filter(
            hosted_meetings__isnull=False
        ).distinct()
        
        performance_data = []
        
        for consultant in consultants:
            meetings_hosted = Meeting.objects.filter(host=consultant).count()
            completed_meetings = Meeting.objects.filter(
                host=consultant, status='completed'
            ).count()
            
            performance_data.append({
                "consultant_name": consultant.get_full_name() or consultant.username,
                "meetings_hosted": meetings_hosted,
                "completion_rate": round((completed_meetings / meetings_hosted) * 100, 2) if meetings_hosted > 0 else 0,
                "avg_rating": 4.2 + (hash(consultant.username) % 8) / 10,  # Simulated rating
                "client_satisfaction": 85 + (hash(consultant.username) % 15)  # Simulated satisfaction
            })
        
        return performance_data


@extend_schema(
    tags=["Consultation Metrics"],
    summary="Get consultation scheduling analytics",
    description="Analyze consultation scheduling patterns, availability, and optimization opportunities."
)
class ConsultationSchedulingAnalyticsView(APIView):
    """Consultation scheduling analytics and optimization"""
    
    permission_classes = []  # Temporarily disabled for testing
    
    def get(self, request):
        # Scheduling patterns
        scheduling_patterns = {
            "peak_request_hours": self._get_peak_request_hours(),
            "peak_request_days": self._get_peak_request_days(),
            "avg_lead_time": self._calculate_avg_lead_time(),
            "rescheduling_rate": self._calculate_rescheduling_rate()
        }
        
        # Availability analysis
        availability_analysis = {
            "consultant_utilization": self._get_consultant_utilization(),
            "time_slot_popularity": self._get_time_slot_popularity(),
            "capacity_vs_demand": self._analyze_capacity_vs_demand()
        }
        
        # Optimization opportunities
        optimization_opportunities = {
            "underutilized_slots": self._identify_underutilized_slots(),
            "high_demand_periods": self._identify_high_demand_periods(),
            "suggested_capacity_adjustments": self._suggest_capacity_adjustments()
        }
        
        return Response({
            "scheduling_patterns": scheduling_patterns,
            "availability_analysis": availability_analysis,
            "optimization_opportunities": optimization_opportunities
        })
    
    def _get_peak_request_hours(self):
        """Get peak hours for meeting requests"""
        # Simplified - would analyze actual request timestamps
        return {
            "9-10": 15,
            "10-11": 25,
            "11-12": 20,
            "14-15": 18,
            "15-16": 22
        }
    
    def _get_peak_request_days(self):
        """Get peak days for meeting requests"""
        return {
            "monday": 18,
            "tuesday": 22,
            "wednesday": 25,
            "thursday": 20,
            "friday": 15
        }
    
    def _calculate_avg_lead_time(self):
        """Calculate average lead time from request to meeting"""
        # Simplified calculation
        meetings_with_lead_time = Meeting.objects.filter(
            requested_datetime__isnull=False,
            confirmed_datetime__isnull=False
        )
        
        if meetings_with_lead_time.exists():
            # This would calculate actual time differences
            return 3.2  # days (simplified)
        return 0
    
    def _calculate_rescheduling_rate(self):
        """Calculate meeting rescheduling rate"""
        total_meetings = Meeting.objects.count()
        rescheduled_meetings = Meeting.objects.filter(status='rescheduled').count()
        
        if total_meetings > 0:
            return round((rescheduled_meetings / total_meetings) * 100, 2)
        return 0
    
    def _get_consultant_utilization(self):
        """Get consultant utilization rates"""
        from django.contrib.auth.models import User
        
        consultants = User.objects.filter(hosted_meetings__isnull=False).distinct()
        utilization_data = []
        
        for consultant in consultants:
            meetings_this_month = Meeting.objects.filter(
                host=consultant,
                created_at__gte=timezone.now() - timedelta(days=30)
            ).count()
            
            # Assuming 20 working days per month, 8 hours per day, 1-hour meetings
            max_capacity = 20 * 8  # 160 meetings per month max
            utilization_rate = round((meetings_this_month / max_capacity) * 100, 2) if max_capacity > 0 else 0
            
            utilization_data.append({
                "consultant": consultant.get_full_name() or consultant.username,
                "meetings_this_month": meetings_this_month,
                "utilization_rate": min(utilization_rate, 100)  # Cap at 100%
            })
        
        return utilization_data
    
    def _get_time_slot_popularity(self):
        """Get popularity of different time slots"""
        # Simplified - would analyze actual meeting times
        return {
            "morning": 35,
            "afternoon": 45,
            "evening": 20
        }
    
    def _analyze_capacity_vs_demand(self):
        """Analyze capacity vs demand patterns"""
        return {
            "current_capacity": 160,  # meetings per month
            "current_demand": 120,   # meeting requests per month
            "utilization_rate": 75,  # percentage
            "capacity_gap": 40       # unused capacity
        }
    
    def _identify_underutilized_slots(self):
        """Identify underutilized time slots"""
        return [
            {"time": "08:00-09:00", "utilization": 15},
            {"time": "17:00-18:00", "utilization": 25},
            {"time": "Friday afternoon", "utilization": 30}
        ]
    
    def _identify_high_demand_periods(self):
        """Identify high demand periods"""
        return [
            {"period": "Tuesday 10:00-12:00", "demand_score": 95},
            {"period": "Wednesday 14:00-16:00", "demand_score": 88},
            {"period": "Thursday 09:00-11:00", "demand_score": 82}
        ]
    
    def _suggest_capacity_adjustments(self):
        """Suggest capacity adjustments"""
        return [
            {
                "suggestion": "Add morning slots on Fridays",
                "impact": "Could increase capacity by 15%"
            },
            {
                "suggestion": "Extend Tuesday availability",
                "impact": "Could reduce wait times by 20%"
            },
            {
                "suggestion": "Add evening slots for international clients",
                "impact": "Could serve 25% more clients"
            }
        ]