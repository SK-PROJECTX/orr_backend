from rest_framework import serializers

from admin_portal.models import Meeting
from drf_spectacular.utils import extend_schema_field

class MeetingPrepSerializer(serializers.Serializer):
    basic_context = serializers.CharField(required=True)
    goals = serializers.CharField(required=True)
    pain_points = serializers.CharField(required=True)


class MeetingRequestSerializer(serializers.ModelSerializer):
    scheduling_url = serializers.URLField(write_only=True, required=False)
    class Meta:
        model = Meeting
        fields = [
            "meeting_type",
            "requested_datetime",
            "agenda",
            "basic_context",
            "goals",
            "pain_points",
            "scheduling_url",
        ]
    def create(self, validated_data):

        scheduling_url = validated_data.pop("scheduling_url", None)
        client = self.context.get("client")

        meeting = Meeting.objects.create(client=client, **validated_data)

        if scheduling_url:
            meeting.meeting_link = scheduling_url
            meeting.save()

        return meeting


class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = "__all__"


class MeetingStatusChangeSerializer(serializers.Serializer):
    status = serializers.CharField(
        help_text="New status value. Must be one of the allowed status choices."
    )

    class Meta:
        model = Meeting
        fields = [
            "status",
        ]


class MeetingCalendarSerializer(serializers.ModelSerializer):
    date = serializers.DateField(source="event_date")
    time = serializers.CharField(source="event_time")
    title = serializers.CharField()
    label = serializers.CharField()
    color = serializers.CharField()

    class Meta:
        model = Meeting
        fields = [
            "id",
            "title",
            "date",
            "time",
            "status",
            "label",
            "color",
            "meeting_link",
        ]



class CalendlyWebhookSerializer(serializers.Serializer):
    webhook_url = serializers.URLField()
    events = serializers.ListField(
        child=serializers.CharField(),
        default=[
            "invitee.created",
            "invitee.canceled",
        ]
    )
    scope = serializers.ChoiceField(choices=["user", "organization"], default="user")