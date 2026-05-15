from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q

from admin_portal.models import Client, ClientDocument, VaultFolder, AuditLog
from ..serializers.client import (
    ClientDocumentSerializer, 
    VaultFolderSerializer,
    DocumentVersionSerializer
)
from common.permissions import IsAdminUser

class VaultDocumentListView(generics.ListCreateAPIView):
    """List all documents or filter by various criteria"""
    serializer_class = ClientDocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = ClientDocument.objects.all().select_related('client', 'folder').prefetch_related('versions')
        
        # Security: Filter by client if not staff/admin
        is_admin = user.is_staff or hasattr(user, 'admin_profile')
        if not is_admin:
            client = getattr(user, 'client_profile', None)
            if client:
                # Clients only see visible documents assigned to them
                queryset = queryset.filter(client=client, visibility='visible')
            else:
                return ClientDocument.objects.none()

        # Filters
        client_id = self.request.query_params.get('client_id')
        if is_admin and client_id:
            queryset = queryset.filter(client_id=client_id)
            
        visibility = self.request.query_params.get('visibility')
        if visibility:
            queryset = queryset.filter(visibility=visibility)
            
        scan_status = self.request.query_params.get('scan_status')
        if scan_status:
            queryset = queryset.filter(scan_status=scan_status)
            
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
            
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(client__company__icontains=search) |
                Q(description__icontains=search)
            )
            
        return queryset.order_by('-created_at')

class VaultFolderListView(generics.ListCreateAPIView):
    """List and create vault folders"""
    queryset = VaultFolder.objects.all()
    serializer_class = VaultFolderSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save()

class VaultActivityListView(APIView):
    """List vault-related activity logs"""
    permission_classes = [IsAdminUser]

    def get(self, request):
        # Filter AuditLog for vault-related models
        logs = AuditLog.objects.filter(
            Q(model_name='ClientDocument') | Q(model_name='VaultFolder')
        ).order_by('-timestamp')[:100]
        
        data = []
        for log in logs:
            data.append({
                'id': log.id,
                'user': log.user.get_full_name() or log.user.username if log.user else 'System',
                'action': log.get_action_display(),
                'item': log.description.split(': ')[-1] if ': ' in log.description else log.description,
                'description': log.description,
                'timestamp': log.timestamp.isoformat(),
                'time': log.timestamp.strftime('%b %d, %H:%M'),
                'model': log.model_name
            })
        return Response(data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def batch_update_documents(request):
    """Batch update metadata or visibility for multiple documents"""
    ids = request.data.get('ids', [])
    updates = request.data.get('updates', {})
    
    if not ids:
        return Response({'error': 'No IDs provided'}, status=status.HTTP_400_BAD_REQUEST)
        
    documents = ClientDocument.objects.filter(id__in=ids)
    count = documents.count()
    
    for doc in documents:
        for key, value in updates.items():
            setattr(doc, key, value)
        doc.save()
        
    # Log the action
    AuditLog.objects.create(
        user=request.user,
        action='update',
        description=f"Batch updated {count} documents: {', '.join(updates.keys())}",
        ip_address=request.META.get('REMOTE_ADDR')
    )
    
    return Response({'message': f'Successfully updated {count} documents'})
