from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Q
from admin_portal.models import Report
from ..serializers.report import ReportSerializer
from rest_framework import permissions
from drf_spectacular.utils import extend_schema, OpenApiParameter



@extend_schema(
    tags=["report"],
    parameters=[
        OpenApiParameter(
            name="status",
            description="Filter reports by status: draft, pending, completed",
            required=False,
            type=str
        ),
        OpenApiParameter(
            name="type",
            description="Filter reports by type (if your model has a type field)",
            required=False,
            type=str
        )
    ]
)
class MeetingReportDashboardView(APIView):
    """
    Endpoint: GET /api/meetings/<meeting_id>/reports/
    Returns reports associated with a specific meeting + summary stats.
    """
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, meeting_id=None):
        reports = Report.objects.filter(meeting_id=meeting_id).order_by('-created_at')
        
        status = request.query_params.get('status')
        report_type = request.query_params.get('type')

        if status:
            reports = reports.filter(status=status.lower())

        if report_type:
            reports = reports.filter(type=report_type.lower())

        reports = reports.order_by('-created_at')   
         
        stats = reports.aggregate(
            total=Count('id'),
            completed=Count('id', filter=Q(status='completed')),
            pending=Count('id', filter=Q(status='pending')),
            draft=Count('id', filter=Q(status='draft'))
        )
        
    
        serializer = ReportSerializer(reports, many=True)
        
      
        return Response({
            "overview": {
                "total_reports": stats['total'],
                "completed": stats['completed'],
                "pending": stats['pending'],
                "draft": stats['draft']
            },
            "reports": serializer.data
        })