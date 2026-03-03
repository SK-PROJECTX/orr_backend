from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Sum, Q
from django.utils import timezone
from ...models import  Project, Wallet, Transaction
from admin_portal.models import Meeting
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from ..services.performance import PerformanceService


@swagger_auto_schema(
        tags=["Dashboard"],
        operation_summary="User Dashboard",
        operation_description="Returns dashboard metrics and summary data for authenticated user."
    )
class DashboardView(APIView):
    def get(self, request):
        user = request.user
        
        meeting_stats = Meeting.objects.filter(host=user).aggregate(
            total=Count('id'),
            completed=Count('id', filter=Q(status='completed')),
            cancelled=Count('id', filter=Q(status='cancelled'))
        )
        
        total_meetings = meeting_stats['total']
        completed = meeting_stats['completed']
        
        engagement_rate = 0
        if total_meetings > 0:
            engagement_rate = int((completed / total_meetings) * 100)

        active_projects_count = Project.objects.filter(
            status='active', 
            client__user=user  # Adjust this filter based on your Client-User relationship
        ).count()

        revenue_stats = Transaction.objects.filter(
            wallet__owner=user,
            transaction_type='payment'
        ).aggregate(total_revenue=Sum('amount'))
        
        total_revenue = revenue_stats['total_revenue'] or 0.00


        try:
            wallet = Wallet.objects.get(owner=user)
            current_balance = wallet.balance
        except Wallet.DoesNotExist:
            current_balance = 0.00

       
        interactions = completed + meeting_stats['cancelled']
        success_rate = 0
        if interactions > 0:
            success_rate = int((completed / interactions) * 100)

        # 6. METRICS: Completed This Month
        # ------------------------------------------------
        current_month = timezone.now().month
        completed_month = Meeting.objects.filter(
            host=user,
            status='completed',
            confirmed_datetime__month=current_month
        ).count()

        # --- CONSTRUCT RESPONSE ---
        data = {
            "total_meetings": {
                "label": "Total Meetings",
                "value": str(total_meetings),
                "trend": "up" # You can add logic to compare vs last month here
            },
            "engagement_rate": {
                "label": "Engagement Rate",
                "value": f"{engagement_rate}%",
                "trend": "up"
            },
            "revenue": {
                "label": "Revenue",
                "value": f"${total_revenue:,.2f}",
                "trend": "up"
            },
            "active_projects": {
                "label": "Active Projects",
                "value": str(active_projects_count),
                "trend": "stable"
            },
            "bottom_stats": {
                "completed_month": completed_month,
                "success_rate": success_rate,
                "active_projects": active_projects_count
            },
            "wallet": {
                "balance": current_balance,
                "currency": "USD" # Or wallet.currency
            }
        }

        return Response(data)
    

@swagger_auto_schema(
        tags=["Dashboard"],
        operation_summary="User Dashboard",
        operation_description="Returns dashboard metrics and summary data for authenticated user."
    )
class PerformanceGraphView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = PerformanceService.get_last_six_months_performance(request.user)
        return Response(data)
