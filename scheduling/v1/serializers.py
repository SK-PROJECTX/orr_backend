# scheduling/serializers.py
from rest_framework import serializers
from ..models import MeetingRequest, MEETING_TYPE_CHOICES
from django.utils.dateparse import parse_datetime
from django.core.exceptions import ValidationError
from django.utils import timezone

class MeetingRequestCreateSerializer(serializers.Serializer):
    calendar = serializers.IntegerField() 
    meeting_type = serializers.ChoiceField(choices=[c[0] for c in MEETING_TYPE_CHOICES])
    preferred_slots = serializers.ListField(
        child=serializers.CharField(), min_length=1
    )
    agenda = serializers.CharField(required=False, allow_blank=True)
    note = serializers.CharField(required=False, allow_blank=True)

    def validate_preferred_slots(self, slots):
        parsed = []
        for s in slots:
            dt = parse_datetime(s)
            if dt is None:
                raise serializers.ValidationError(f"Invalid datetime: {s}")
            if timezone.is_naive(dt):
                raise serializers.ValidationError("Datetime must include timezone information (ISO tz).")
            if dt <= timezone.now():
                raise serializers.ValidationError("All preferred slots must be in the future.")
            parsed.append(dt)
        return parsed
