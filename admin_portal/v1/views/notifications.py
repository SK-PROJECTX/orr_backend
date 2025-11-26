from django.db.models import Q, Count
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from admin_portal.models import SystemNotification
from ..serializers.notifications import (
    NotificationListSerializer, NotificationDetailSerializer
)


@extend_schema(
    tags=["Notifications"],
    summary="List user notifications",
    description="Retrieve a filtered list of notifications for the current user with options to filter by read status and notification type."
)
class NotificationListView(generics.ListAPIView):
    """List user notifications"""
    serializer_class = NotificationListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = SystemNotification.objects.filter(
            recipient=self.request.user
        ).select_related('related_ticket', 'related_meeting', 'related_client')
        
        # Filter by read status
        is_read = self.request.query_params.get('is_read', None)
        if is_read is not None:
            queryset = queryset.filter(is_read=is_read.lower() == 'true')
        
        # Filter by notification type
        notification_type = self.request.query_params.get('type', None)
        if notification_type:
            queryset = queryset.filter(notification_type=notification_type)
        
        return queryset.order_by('-created_at')


@extend_schema(
    tags=["Notifications"],
    summary="Get notification details",
    description="Retrieve detailed information about a specific notification including related object information (tickets, meetings, clients)."
)
class NotificationDetailView(generics.RetrieveAPIView):
    """Get notification details"""
    serializer_class = NotificationDetailSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return SystemNotification.objects.filter(recipient=self.request.user)


@extend_schema(
    tags=["Notifications"],
    summary="Perform notification actions",
    description="Execute actions on individual notifications including mark as read or unread."
)
class NotificationActionsView(APIView):
    """Notification management actions"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        try:
            notification = SystemNotification.objects.get(
                pk=pk, 
                recipient=request.user
            )
            action = request.data.get('action')
            
            if action == 'mark_read':
                notification.is_read = True
                notification.save()
                return Response({'message': 'Notification marked as read'})
            
            elif action == 'mark_unread':
                notification.is_read = False
                notification.save()
                return Response({'message': 'Notification marked as unread'})
            
            else:
                return Response(
                    {'error': 'Invalid action'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
                
        except SystemNotification.DoesNotExist:
            return Response(
                {'error': 'Notification not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )


@extend_schema(
    tags=["Notifications"],
    summary="Perform bulk notification actions",
    description="Execute bulk operations on notifications including mark all as read, delete read notifications, or delete all notifications."
)
class NotificationBulkActionsView(APIView):
    """Bulk notification actions"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        action = request.data.get('action')
        notification_ids = request.data.get('notification_ids', [])
        
        queryset = SystemNotification.objects.filter(
            recipient=request.user
        )
        
        if notification_ids:
            queryset = queryset.filter(id__in=notification_ids)
        
        if action == 'mark_all_read':
            count = queryset.update(is_read=True)
            return Response({'message': f'Marked {count} notifications as read'})
        
        elif action == 'delete_read':
            count = queryset.filter(is_read=True).delete()[0]
            return Response({'message': f'Deleted {count} read notifications'})
        
        elif action == 'delete_all':
            count = queryset.delete()[0]
            return Response({'message': f'Deleted {count} notifications'})
        
        else:
            return Response(
                {'error': 'Invalid action'}, 
                status=status.HTTP_400_BAD_REQUEST
            )


@extend_schema(
    tags=["Notifications"],
    summary="Get notification statistics",
    description="Retrieve notification statistics for the current user including total count, unread count, and distribution by notification type."
)
class NotificationStatsView(APIView):
    """Notification statistics"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user_notifications = SystemNotification.objects.filter(
            recipient=request.user
        )
        
        stats = {
            'total_notifications': user_notifications.count(),
            'unread_notifications': user_notifications.filter(is_read=False).count(),
            'notifications_by_type': dict(
                user_notifications.values('notification_type')
                .annotate(count=Count('id'))
                .values_list('notification_type', 'count')
            ),
        }
        
        return Response(stats)