from rest_framework import serializers

from admin_portal.models import Meeting


class MeetingListSerializer(serializers.ModelSerializer):
    """Meeting list view serializer"""

    client_name = serializers.SerializerMethodField()
    client_company = serializers.SerializerMethodField()
    host_name = serializers.SerializerMethodField()
    
    def get_client_name(self, obj):
        if obj.client and obj.client.user:
            full_name = obj.client.user.get_full_name().strip()
            if full_name:
                return full_name
            return obj.client.user.username or "Unknown Client"
        return "Unknown Client"
    
    def get_client_company(self, obj):
        if obj.client:
            return obj.client.company or "N/A"
        return "N/A"
    
    def get_host_name(self, obj):
        if obj.host:
            full_name = obj.host.get_full_name().strip()
            if full_name:
                return full_name
            return obj.host.username or "Unknown Host"
        return None

    class Meta:
        model = Meeting
        fields = [
            "id",
            "client_name",
            "client_company",
            "meeting_type",
            "status",
            "requested_datetime",
            "confirmed_datetime",
            "duration_minutes",
            "host_name",
            "created_at",
        ]


class MeetingDetailSerializer(serializers.ModelSerializer):
    """Detailed meeting view serializer"""

    client_name = serializers.SerializerMethodField()
    client_email = serializers.SerializerMethodField()
    client_company = serializers.SerializerMethodField()
    host_name = serializers.SerializerMethodField()
    
    def get_client_name(self, obj):
        if obj.client and obj.client.user:
            full_name = obj.client.user.get_full_name().strip()
            if full_name:
                return full_name
            return obj.client.user.username or "Unknown Client"
        return "Unknown Client"
    
    def get_client_email(self, obj):
        if obj.client and obj.client.user:
            return obj.client.user.email
        return "N/A"
    
    def get_client_company(self, obj):
        if obj.client:
            return obj.client.company or "N/A"
        return "N/A"
    
    def get_host_name(self, obj):
        if obj.host:
            full_name = obj.host.get_full_name().strip()
            if full_name:
                return full_name
            return obj.host.username or "Unknown Host"
        return None

    class Meta:
        model = Meeting
        fields = [
            "id",
            "client_name",
            "client_email",
            "client_company",
            "meeting_type",
            "status",
            "requested_datetime",
            "confirmed_datetime",
            "duration_minutes",
            "agenda",
            "meeting_notes",
            "internal_notes",
            "host_name",
            "calendar_event_id",
            "meeting_link",
            "created_at",
            "updated_at",
        ]


class MeetingCreateSerializer(serializers.ModelSerializer):
    """Meeting creation serializer"""
    
    client_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Meeting
        fields = [
            "client_id",
            "meeting_type",
            "requested_datetime",
            "duration_minutes",
            "agenda",
            "meeting_notes",
            "internal_notes",
            "meeting_link",
        ]
        extra_kwargs = {
            'meeting_notes': {'required': False, 'allow_blank': True},
            'internal_notes': {'required': False, 'allow_blank': True},
            'meeting_link': {'required': False, 'allow_blank': True},
        }
        
    def validate_client_id(self, value):
        from admin_portal.models import Client
        
        try:
            Client.objects.get(id=value)
        except Client.DoesNotExist:
            raise serializers.ValidationError("Client with this ID not found")
        return value


class MeetingUpdateSerializer(serializers.ModelSerializer):
    """Meeting update serializer"""

    class Meta:
        model = Meeting
        fields = [
            "status",
            "confirmed_datetime",
            "duration_minutes",
            "host",
            "meeting_notes",
            "internal_notes",
            "meeting_link",
        ]


class MeetingActionSerializer(serializers.Serializer):
    """Meeting action serializer"""

    action = serializers.ChoiceField(
        choices=["confirm", "reschedule", "decline", "complete", "cancel"]
    )
    confirmed_datetime = serializers.DateTimeField(required=False)
    notes = serializers.CharField(required=False, allow_blank=True)


class MeetingStatsSerializer(serializers.Serializer):
    """Meeting statistics serializer"""

    total_meetings = serializers.IntegerField()
    requested_meetings = serializers.IntegerField()
    confirmed_meetings = serializers.IntegerField()
    completed_meetings = serializers.IntegerField()
    cancelled_meetings = serializers.IntegerField()
    avg_confirmation_time = serializers.FloatField()
    meetings_by_type = serializers.DictField()
    upcoming_meetings = serializers.ListField()
