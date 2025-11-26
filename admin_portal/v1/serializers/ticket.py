from rest_framework import serializers
from admin_portal.models import Ticket, TicketMessage


class TicketListSerializer(serializers.ModelSerializer):
    """Ticket list view serializer"""
    client_name = serializers.CharField(source='client.user.get_full_name')
    client_company = serializers.CharField(source='client.company')
    assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', allow_null=True)
    messages_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Ticket
        fields = [
            'id', 'ticket_id', 'subject', 'status', 'priority', 'source',
            'client_name', 'client_company', 'assigned_to_name', 
            'messages_count', 'created_at', 'updated_at'
        ]
    
    def get_messages_count(self, obj):
        return obj.messages.count()


class TicketDetailSerializer(serializers.ModelSerializer):
    """Detailed ticket view serializer"""
    client_name = serializers.CharField(source='client.user.get_full_name')
    client_email = serializers.CharField(source='client.user.email')
    client_company = serializers.CharField(source='client.company')
    assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', allow_null=True)
    related_meeting_info = serializers.SerializerMethodField()
    related_content_info = serializers.SerializerMethodField()
    
    class Meta:
        model = Ticket
        fields = [
            'id', 'ticket_id', 'subject', 'description', 'status', 'priority', 
            'source', 'client_name', 'client_email', 'client_company',
            'assigned_to_name', 'internal_notes', 'related_meeting_info',
            'related_content_info', 'created_at', 'updated_at'
        ]
    
    def get_related_meeting_info(self, obj):
        if obj.related_meeting:
            return {
                'id': obj.related_meeting.id,
                'type': obj.related_meeting.meeting_type,
                'datetime': obj.related_meeting.confirmed_datetime or obj.related_meeting.requested_datetime
            }
        return None
    
    def get_related_content_info(self, obj):
        if obj.related_content:
            return {
                'id': obj.related_content.id,
                'title': obj.related_content.title,
                'type': obj.related_content.content_type
            }
        return None


class TicketUpdateSerializer(serializers.ModelSerializer):
    """Ticket update serializer"""
    
    class Meta:
        model = Ticket
        fields = ['status', 'priority', 'assigned_to', 'internal_notes', 'related_meeting', 'related_content']


class TicketMessageSerializer(serializers.ModelSerializer):
    """Ticket message serializer"""
    sender_name = serializers.CharField(source='sender.get_full_name')
    sender_type = serializers.SerializerMethodField()
    
    class Meta:
        model = TicketMessage
        fields = [
            'id', 'message', 'sender_name', 'sender_type', 'is_internal', 'created_at'
        ]
    
    def get_sender_type(self, obj):
        # Determine if sender is admin or client
        if hasattr(obj.sender, 'admin_profile'):
            return 'admin'
        return 'client'


class TicketCreateSerializer(serializers.ModelSerializer):
    """Create new ticket serializer"""
    
    class Meta:
        model = Ticket
        fields = ['client', 'subject', 'description', 'priority', 'source', 'assigned_to']


class TicketStatsSerializer(serializers.Serializer):
    """Ticket statistics serializer"""
    total_tickets = serializers.IntegerField()
    new_tickets = serializers.IntegerField()
    in_progress_tickets = serializers.IntegerField()
    waiting_client_tickets = serializers.IntegerField()
    resolved_tickets = serializers.IntegerField()
    avg_response_time = serializers.FloatField()
    avg_resolution_time = serializers.FloatField()
    tickets_by_priority = serializers.DictField()
    tickets_by_source = serializers.DictField()