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
            # Try to get client from either client_profile or profile attribute
            client = getattr(user, 'client_profile', None) or getattr(user, 'profile', None)
            
            # If the profile doesn't have a direct Client relation (e.g. it's the client.models.Profile),
            # we might need to find the Client record.
            if not isinstance(client, Client) and client:
                 client = Client.objects.filter(user=user).first()

            if client:
                # Clients only see documents explicitly marked as client-facing
                queryset = queryset.filter(client=client, visibility='client')
            else:
                return ClientDocument.objects.none()

        # Filters
        client_id = self.request.query_params.get('client_id')
        if is_admin and client_id:
            queryset = queryset.filter(client_id=client_id)
            
        folder_id = self.request.query_params.get('folder_id')
        if folder_id:
            queryset = queryset.filter(folder_id=folder_id)
            
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
    serializer_class = VaultFolderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = VaultFolder.objects.all()
        
        is_admin = user.is_staff or hasattr(user, 'admin_profile')
        if not is_admin:
            client = getattr(user, 'client_profile', None) or getattr(user, 'profile', None)
            
            if not isinstance(client, Client) and client:
                 client = Client.objects.filter(user=user).first()

            if client:
                # Clients only see folders explicitly assigned to them or global folders
                queryset = queryset.filter(Q(client=client) | Q(client__isnull=True))
            else:
                return VaultFolder.objects.none()
        
        return queryset

    def perform_create(self, serializer):
        serializer.save()

class VaultActivityListView(APIView):
    """List vault-related activity logs"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        is_admin = user.is_staff or hasattr(user, 'admin_profile')
        
        # Filter AuditLog for vault-related models
        queryset = AuditLog.objects.filter(
            Q(model_name='ClientDocument') | Q(model_name='VaultFolder')
        )
        
        if not is_admin:
            # Try to get client
            client = getattr(user, 'client_profile', None) or getattr(user, 'profile', None)
            if not isinstance(client, Client) and client:
                 client = Client.objects.filter(user=user).first()
            
            if client:
                # Filter by logs where the user is the client
                queryset = queryset.filter(user=user)
            else:
                return Response({"status": 200, "message": "Success", "data": []})

        logs = queryset.order_by('-timestamp')[:100]
        
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

class VaultDocumentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a vault document"""
    serializer_class = ClientDocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = ClientDocument.objects.all().select_related('client', 'folder').prefetch_related('versions')
        
        is_admin = user.is_staff or hasattr(user, 'admin_profile')
        if not is_admin:
            client = getattr(user, 'client_profile', None) or getattr(user, 'profile', None)
            if not isinstance(client, Client) and client:
                 client = Client.objects.filter(user=user).first()

            if client:
                queryset = queryset.filter(client=client, visibility='client')
            else:
                return ClientDocument.objects.none()
        
        return queryset
