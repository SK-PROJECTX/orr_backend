import csv
import json
from io import StringIO
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_spectacular.utils import extend_schema

from admin_portal.models import Client, Ticket, Meeting, AIConversation, ClientDocument, AuditLog
from admin_portal.permissions import CanManageSettings
from common.permissions import IsAdminUser


@extend_schema(
    tags=["Compliance & Data Management"],
    summary="Export client data for GDPR compliance",
    description="Export all data associated with a specific client for GDPR data portability requests."
)
class ClientDataExportView(APIView):
    """Export client data for GDPR compliance"""
    permission_classes = [IsAdminUser, CanManageSettings]
    
    def post(self, request):
        client_id = request.data.get('client_id')
        export_format = request.data.get('format', 'json')  # json or csv
        
        try:
            client = Client.objects.select_related('user').get(id=client_id)
        except Client.DoesNotExist:
            return Response(
                {'error': 'Client not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Collect all client data
        client_data = {
            'personal_info': {
                'id': client.id,
                'first_name': client.user.first_name,
                'last_name': client.user.last_name,
                'email': client.user.email,
                'company': client.company,
                'role': client.role,
                'stage': client.stage,
                'primary_pillar': client.primary_pillar,
                'secondary_pillars': client.secondary_pillars,
                'created_at': client.created_at.isoformat(),
                'last_activity': client.last_activity.isoformat() if client.last_activity else None,
            },
            'tickets': list(
                client.tickets.values(
                    'ticket_id', 'subject', 'status', 'priority', 
                    'description', 'created_at', 'updated_at'
                )
            ),
            'meetings': list(
                client.meetings.values(
                    'meeting_type', 'status', 'requested_datetime',
                    'confirmed_datetime', 'agenda', 'created_at'
                )
            ),
            'ai_conversations': list(
                client.ai_conversations.values(
                    'session_id', 'summary', 'escalated_to_ticket', 'created_at'
                )
            ),
            'documents': list(
                client.documents.values(
                    'title', 'description', 'document_type', 
                    'is_visible_to_client', 'created_at'
                )
            )
        }
        
        # Create audit log
        AuditLog.objects.create(
            user=request.user,
            action='data_export',
            model_name='Client',
            object_id=str(client.id),
            description=f'Data export for client: {client.user.get_full_name()}',
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        if export_format == 'csv':
            return self._export_as_csv(client_data, client)
        else:
            return Response({
                'client_data': client_data,
                'export_timestamp': timezone.now().isoformat(),
                'exported_by': request.user.get_full_name()
            })
    
    def _export_as_csv(self, client_data, client):
        """Export data as CSV file"""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="client_data_{client.id}.csv"'
        
        writer = csv.writer(response)
        
        # Personal info
        writer.writerow(['Personal Information'])
        for key, value in client_data['personal_info'].items():
            writer.writerow([key, value])
        
        writer.writerow([])  # Empty row
        
        # Tickets
        writer.writerow(['Tickets'])
        if client_data['tickets']:
            writer.writerow(client_data['tickets'][0].keys())
            for ticket in client_data['tickets']:
                writer.writerow(ticket.values())
        
        writer.writerow([])  # Empty row
        
        # Meetings
        writer.writerow(['Meetings'])
        if client_data['meetings']:
            writer.writerow(client_data['meetings'][0].keys())
            for meeting in client_data['meetings']:
                writer.writerow(meeting.values())
        
        return response


@extend_schema(
    tags=["Compliance & Data Management"],
    summary="Delete client data for GDPR compliance",
    description="Permanently delete all data associated with a client for GDPR right to be forgotten requests."
)
class ClientDataDeletionView(APIView):
    """Delete client data for GDPR compliance"""
    permission_classes = [IsAdminUser, CanManageSettings]
    
    def post(self, request):
        client_id = request.data.get('client_id')
        confirmation = request.data.get('confirmation', '')
        
        if confirmation != 'DELETE_ALL_DATA':
            return Response(
                {'error': 'Confirmation string required: DELETE_ALL_DATA'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            client = Client.objects.select_related('user').get(id=client_id)
        except Client.DoesNotExist:
            return Response(
                {'error': 'Client not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Create audit log before deletion
        AuditLog.objects.create(
            user=request.user,
            action='data_delete',
            model_name='Client',
            object_id=str(client.id),
            description=f'GDPR data deletion for client: {client.user.get_full_name()}',
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        # Delete related data (cascade should handle most of this)
        client_name = client.user.get_full_name()
        user = client.user
        
        # Delete the client (this will cascade to related objects)
        client.delete()
        
        # Delete the user account
        user.delete()
        
        return Response({
            'message': f'All data for client {client_name} has been permanently deleted',
            'deleted_at': timezone.now().isoformat(),
            'deleted_by': request.user.get_full_name()
        })


@extend_schema(
    tags=["Compliance & Data Management"],
    summary="Generate compliance report",
    description="Generate a compliance report showing data handling activities and audit trail."
)
class ComplianceReportView(APIView):
    """Generate compliance reports"""
    permission_classes = [IsAdminUser, CanManageSettings]
    
    def get(self, request):
        # Data handling statistics
        total_clients = Client.objects.count()
        active_clients = Client.objects.filter(is_portal_active=True).count()
        
        # Recent audit activities
        recent_audits = AuditLog.objects.filter(
            action__in=['data_export', 'data_delete']
        ).order_by('-timestamp')[:20]
        
        # Data retention info
        data_retention_info = {
            'total_clients': total_clients,
            'active_clients': active_clients,
            'inactive_clients': total_clients - active_clients,
            'total_tickets': Ticket.objects.count(),
            'total_meetings': Meeting.objects.count(),
            'total_ai_conversations': AIConversation.objects.count(),
            'total_documents': ClientDocument.objects.count(),
        }
        
        return Response({
            'data_retention_info': data_retention_info,
            'recent_compliance_activities': [
                {
                    'user': audit.user.get_full_name() if audit.user else 'System',
                    'action': audit.get_action_display(),
                    'description': audit.description,
                    'timestamp': audit.timestamp.isoformat(),
                    'ip_address': audit.ip_address
                }
                for audit in recent_audits
            ],
            'generated_at': timezone.now().isoformat(),
            'generated_by': request.user.get_full_name()
        })