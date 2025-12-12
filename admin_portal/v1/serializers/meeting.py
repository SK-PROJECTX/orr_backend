from rest_framework import serializers

from admin_portal.models import Meeting


class MeetingListSerializer(serializers.ModelSerializer):
    """Meeting list view serializer"""

    client_name = serializers.CharField(source="client.user.get_full_name")
    client_company = serializers.CharField(source="client.company")
    host_name = serializers.CharField(source="host.get_full_name", allow_null=True)

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

    client_name = serializers.CharField(source="client.user.get_full_name")
    client_email = serializers.CharField(source="client.user.email")
    client_company = serializers.CharField(source="client.company")
    host_name = serializers.CharField(source="host.get_full_name", allow_null=True)

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
    
    client_email = serializers.EmailField(write_only=True)
    
    class Meta:
        model = Meeting
        fields = [
            "client_email",
            "meeting_type",
            "requested_datetime",
            "duration_minutes",
            "agenda",
        ]
        
    def validate_client_email(self, value):
        from django.contrib.auth.models import User
        from admin_portal.models import Client
        
        try:
            user = User.objects.get(email=value)
            Client.objects.get(user=user)
        except (User.DoesNotExist, Client.DoesNotExist):
            raise serializers.ValidationError("Client with this email not found")
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
