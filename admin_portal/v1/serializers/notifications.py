from rest_framework import serializers
from admin_portal.models import SystemNotification


class NotificationListSerializer(serializers.ModelSerializer):
    """Notification list serializer"""
    related_object_info = serializers.SerializerMethodField()
    
    class Meta:
        model = SystemNotification
        fields = [
            'id', 'notification_type', 'title', 'message', 'is_read',
            'created_at', 'related_object_info'
        ]
    
    def get_related_object_info(self, obj):
        """Get related object information"""
        if obj.related_ticket:
            return {
                'type': 'ticket',
                'id': obj.related_ticket.id,
                'identifier': obj.related_ticket.ticket_id
            }
        elif obj.related_meeting:
            return {
                'type': 'meeting',
                'id': obj.related_meeting.id,
                'identifier': f"{obj.related_meeting.client.user.get_full_name()} - {obj.related_meeting.meeting_type}"
            }
        elif obj.related_client:
            return {
                'type': 'client',
                'id': obj.related_client.id,
                'identifier': f"{obj.related_client.user.get_full_name()} - {obj.related_client.company}"
            }
        return None


class NotificationDetailSerializer(serializers.ModelSerializer):
    """Detailed notification serializer"""
    related_ticket_info = serializers.SerializerMethodField()
    related_meeting_info = serializers.SerializerMethodField()
    related_client_info = serializers.SerializerMethodField()
    
    class Meta:
        model = SystemNotification
        fields = [
            'id', 'notification_type', 'title', 'message', 'is_read',
            'created_at', 'related_ticket_info', 'related_meeting_info',
            'related_client_info'
        ]
    
    def get_related_ticket_info(self, obj):
        if obj.related_ticket:
            return {
                'id': obj.related_ticket.id,
                'ticket_id': obj.related_ticket.ticket_id,
                'subject': obj.related_ticket.subject,
                'status': obj.related_ticket.status
            }
        return None
    
    def get_related_meeting_info(self, obj):
        if obj.related_meeting:
            return {
                'id': obj.related_meeting.id,
                'meeting_type': obj.related_meeting.meeting_type,
                'status': obj.related_meeting.status,
                'datetime': obj.related_meeting.confirmed_datetime or obj.related_meeting.requested_datetime
            }
        return None
    
    def get_related_client_info(self, obj):
        if obj.related_client:
            return {
                'id': obj.related_client.id,
                'name': obj.related_client.user.get_full_name(),
                'company': obj.related_client.company,
                'email': obj.related_client.user.email
            }
        return None