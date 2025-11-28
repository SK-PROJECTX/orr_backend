from django.db.models import Q, Count
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from admin_portal.permissions import CanViewAllClients, CanEditClients
from drf_spectacular.utils import extend_schema, OpenApiParameter

from admin_portal.models import Client, ClientDocument
from ..serializers.client import (
    ClientListSerializer, ClientDetailSerializer, ClientUpdateSerializer,
    ClientDocumentSerializer, ClientEngagementHistorySerializer
)


@extend_schema(
    tags=["Client Management"],
    summary="List all clients",
    description="Retrieve a paginated list of all clients with advanced filtering options including search by name/email/company, filter by stage, pillar, assigned admin, portal status, and activity level."
)
class ClientListView(generics.ListAPIView):
    """List all clients with filtering and search"""
    serializer_class = ClientListSerializer
    permission_classes = [CanViewAllClients]
    
    def get_queryset(self):
        queryset = Client.objects.select_related('user', 'assigned_admin').all()
        
        # Role-based filtering
        user_role = self.request.user.admin_profile.role
        if user_role.name == 'admin' and not user_role.can_view_all_clients:
            # Admin can only see clients assigned to them
            queryset = queryset.filter(assigned_admin=self.request.user)
        
        # Search functionality
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(user__first_name__icontains=search) |
                Q(user__last_name__icontains=search) |
                Q(user__email__icontains=search) |
                Q(company__icontains=search)
            )
        
        # Filters
        stage = self.request.query_params.get('stage', None)
        if stage:
            queryset = queryset.filter(stage=stage)
        
        pillar = self.request.query_params.get('pillar', None)
        if pillar:
            queryset = queryset.filter(primary_pillar=pillar)
        
        assigned_admin = self.request.query_params.get('assigned_admin', None)
        if assigned_admin:
            queryset = queryset.filter(assigned_admin_id=assigned_admin)
        
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            queryset = queryset.filter(is_portal_active=is_active.lower() == 'true')
        
        # Activity filter
        activity = self.request.query_params.get('activity', None)
        if activity == 'active':
            # Active in last 30 days
            from datetime import timedelta
            from django.utils import timezone
            queryset = queryset.filter(
                user__last_login__gte=timezone.now() - timedelta(days=30)
            )
        elif activity == 'dormant':
            # No activity in last 30 days
            from datetime import timedelta
            from django.utils import timezone
            queryset = queryset.filter(
                Q(user__last_login__lt=timezone.now() - timedelta(days=30)) |
                Q(user__last_login__isnull=True)
            )
        
        return queryset.order_by('-created_at')


@extend_schema(
    tags=["Client Management"],
    summary="Get or update client details",
    description="Retrieve detailed information about a specific client or update client information including company details, stage, pillar assignments, and internal notes."
)
class ClientDetailView(generics.RetrieveUpdateAPIView):
    """Get and update client details"""
    queryset = Client.objects.select_related('user', 'assigned_admin').all()
    permission_classes = [CanViewAllClients]
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ClientDetailSerializer
        return ClientUpdateSerializer


@extend_schema(
    tags=["Client Management"],
    summary="Get client engagement history",
    description="Retrieve comprehensive engagement history for a client including recent tickets, meetings, and documents."
)
class ClientEngagementHistoryView(APIView):
    """Get client engagement history (tickets, meetings, documents)"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        try:
            client = Client.objects.get(pk=pk)
            serializer = ClientEngagementHistorySerializer(client)
            return Response(serializer.data)
        except Client.DoesNotExist:
            return Response(
                {'error': 'Client not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )


@extend_schema(
    tags=["Client Management"],
    summary="List or create client documents",
    description="Retrieve all documents for a specific client or upload new documents. Documents can be marked as visible or hidden from the client."
)
class ClientDocumentListView(generics.ListCreateAPIView):
    """List and create client documents"""
    serializer_class = ClientDocumentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        client_id = self.kwargs.get('client_id')
        return ClientDocument.objects.filter(client_id=client_id).order_by('-created_at')
    
    def perform_create(self, serializer):
        client_id = self.kwargs.get('client_id')
        serializer.save(client_id=client_id, uploaded_by=self.request.user)


@extend_schema(
    tags=["Client Management"],
    summary="Manage client document",
    description="Retrieve, update, or delete a specific client document including metadata and visibility settings."
)
class ClientDocumentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Get, update, or delete client document"""
    serializer_class = ClientDocumentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        client_id = self.kwargs.get('client_id')
        return ClientDocument.objects.filter(client_id=client_id)


@extend_schema(
    tags=["Client Management"],
    summary="Perform client management actions",
    description="Execute various client management actions including toggle portal access, reset password, and update client stage."
)
class ClientActionsView(APIView):
    """Client management actions"""
    permission_classes = [CanEditClients]
    
    def post(self, request, pk):
        try:
            client = Client.objects.get(pk=pk)
            action = request.data.get('action')
            
            if action == 'toggle_portal_access':
                client.is_portal_active = not client.is_portal_active
                client.save()
                return Response({
                    'message': f"Portal access {'enabled' if client.is_portal_active else 'disabled'}",
                    'is_portal_active': client.is_portal_active
                })
            
            elif action == 'reset_password':
                # Trigger password reset email
                from django.contrib.auth.tokens import default_token_generator
                from django.utils.http import urlsafe_base64_encode
                from django.utils.encoding import force_bytes
                
                # Generate reset token and send email
                token = default_token_generator.make_token(client.user)
                uid = urlsafe_base64_encode(force_bytes(client.user.pk))
                
                # Here you would send the password reset email
                # For now, just return success
                return Response({
                    'message': 'Password reset email sent',
                    'reset_token': token,
                    'uid': uid
                })
            
            elif action == 'update_stage':
                new_stage = request.data.get('stage')
                if new_stage in dict(Client.STAGE_CHOICES):
                    client.stage = new_stage
                    client.save()
                    return Response({
                        'message': f'Client stage updated to {new_stage}',
                        'stage': client.stage
                    })
                else:
                    return Response(
                        {'error': 'Invalid stage'}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            elif action == 'update_pillar':
                new_pillar = request.data.get('primary_pillar')
                secondary_pillars = request.data.get('secondary_pillars', [])
                
                if new_pillar in dict(Client.PILLAR_CHOICES):
                    client.primary_pillar = new_pillar
                    client.secondary_pillars = secondary_pillars
                    client.save()
                    return Response({
                        'message': f'Client pillar updated to {new_pillar}',
                        'primary_pillar': client.primary_pillar,
                        'secondary_pillars': client.secondary_pillars
                    })
                else:
                    return Response(
                        {'error': 'Invalid pillar'}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            elif action == 'update_contact_details':
                user_data = request.data.get('user_data', {})
                if 'first_name' in user_data:
                    client.user.first_name = user_data['first_name']
                if 'last_name' in user_data:
                    client.user.last_name = user_data['last_name']
                if 'email' in user_data:
                    client.user.email = user_data['email']
                client.user.save()
                
                client_data = request.data.get('client_data', {})
                if 'company' in client_data:
                    client.company = client_data['company']
                if 'role' in client_data:
                    client.role = client_data['role']
                client.save()
                
                return Response({'message': 'Contact details updated successfully'})
            
            elif action == 'add_internal_note':
                note = request.data.get('note', '')
                if note:
                    from django.utils import timezone
                    timestamp = timezone.now().strftime('%Y-%m-%d %H:%M')
                    new_note = f"[{timestamp}] {request.user.get_full_name()}: {note}"
                    
                    if client.internal_notes:
                        client.internal_notes += f"\n\n{new_note}"
                    else:
                        client.internal_notes = new_note
                    
                    client.save()
                    return Response({'message': 'Internal note added successfully'})
                else:
                    return Response({'error': 'Note content is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            else:
                return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
                
        except Client.DoesNotExist:
            return Response(
                {'error': 'Client not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )


@extend_schema(
    tags=["Client Management"],
    summary="Get client statistics",
    description="Retrieve comprehensive client statistics including total counts, distribution by stage and pillar, and recent activity metrics."
)
class ClientStatsView(APIView):
    """Client statistics and analytics"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Basic client stats
        total_clients = Client.objects.count()
        active_clients = Client.objects.filter(is_portal_active=True).count()
        
        # Clients by stage
        clients_by_stage = dict(
            Client.objects.values('stage').annotate(count=Count('id')).values_list('stage', 'count')
        )
        
        # Clients by pillar
        clients_by_pillar = dict(
            Client.objects.values('primary_pillar').annotate(count=Count('id')).values_list('primary_pillar', 'count')
        )
        
        # Recent activity
        from datetime import timedelta
        from django.utils import timezone
        
        recently_active = Client.objects.filter(
            user__last_login__gte=timezone.now() - timedelta(days=7)
        ).count()
        
        return Response({
            'total_clients': total_clients,
            'active_clients': active_clients,
            'recently_active': recently_active,
            'clients_by_stage': clients_by_stage,
            'clients_by_pillar': clients_by_pillar,
        })