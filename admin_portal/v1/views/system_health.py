from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from admin_portal.permissions import CanManageSettings
from admin_portal.services import SystemHealthService


@extend_schema(
    tags=["System Health"],
    summary="Get system health status",
    description="Retrieve comprehensive system health metrics including database status, recent errors, and performance indicators.",
)
class SystemHealthView(APIView):
    """System health monitoring"""

    permission_classes = [IsAuthenticated, CanManageSettings]

    def get(self, request):
        health_data = SystemHealthService.get_system_health()
        return Response(health_data)


@extend_schema(
    tags=["System Health"],
    summary="Get system performance metrics",
    description="Retrieve detailed performance metrics for system monitoring and optimization.",
)
class SystemPerformanceView(APIView):
    """System performance metrics"""

    permission_classes = [IsAuthenticated, CanManageSettings]

    def get(self, request):
        from datetime import timedelta

        from django.db import connection
        from django.utils import timezone

        # Database query performance
        queries_count = len(connection.queries)

        # Recent activity metrics
        now = timezone.now()
        last_hour = now - timedelta(hours=1)

        from admin_portal.models import AuditLog, SystemNotification

        recent_activities = {
            "audit_logs_last_hour": AuditLog.objects.filter(
                timestamp__gte=last_hour
            ).count(),
            "notifications_last_hour": SystemNotification.objects.filter(
                created_at__gte=last_hour
            ).count(),
            "database_queries": queries_count,
        }

        return Response(
            {"performance_metrics": recent_activities, "timestamp": now.isoformat()}
        )
