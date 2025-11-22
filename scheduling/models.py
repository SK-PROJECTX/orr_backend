from django.db import models
from organization.models import Organization
from common.models import Audit
from django.conf import settings
from django.urls import reverse
from django.core.validators import MinValueValidator
from django.utils import timezone

User = settings.AUTH_USER_MODEL

class Calendar(Audit):
    """
    A calendar belongs to an Organization or a User (personal calendar).
    """
    name = models.CharField(max_length=255)
    owner_org = models.ForeignKey(Organization, null=True, blank=True, on_delete=models.CASCADE, related_name="calendars")
    owner_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name="calendars")
    timezone = models.CharField(max_length=64, default="UTC")
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
class CalendarSlot(Audit):
    """
    Pre-generated time slot. Each slot is atomic and can be booked.
    """
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE, related_name="slots")
    start = models.DateTimeField()
    end = models.DateTimeField()
    is_available = models.BooleanField(default=True)
    label = models.CharField(max_length=255, blank=True)
    metadata = models.JSONField(default=dict, blank=True)


    class Meta:
        indexes = [
            models.Index(fields=["calendar", "start", "end"]),
        ]
        ordering = ["start"]

    def __str__(self):
        return f"Slot {self.pk} - {self.start.isoformat()} -> {self.end.isoformat()}"


    
class Event(Audit):
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="created_events")
    attendees = models.ManyToManyField(User, blank=True, related_name="events")
    recurrence_rule = models.CharField(max_length=512, blank=True)
    recurrence_end = models.DateTimeField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)  
    cancelled = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=["start"]),
            models.Index(fields=["end"]),
            models.Index(fields=["created_by"]),
        ]

    def __str__(self):
        return f"{self.title} ({self.start.isoformat()})"

    def get_ics_url(self):
        return reverse("scheduling-event-ics", kwargs={"pk": self.pk})
    


class Availability(Audit):
    """
    Organization or user availability block. Useful for blocking free/busy slots.
    """
    owner_user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name="availabilities")
    owner_org = models.ForeignKey(Organization, null=True, blank=True, on_delete=models.CASCADE, related_name="availabilities")
    start = models.DateTimeField()
    end = models.DateTimeField()
    is_free = models.BooleanField(default=False)  
    recurrence_rule = models.CharField(max_length=512, blank=True)
    note = models.TextField(blank=True)

    class Meta:
        indexes = [models.Index(fields=["start", "end"])]



MEETING_TYPE_CHOICES = [
    ("first_meeting", "First meeting / Discovery"),
    ("follow_up", "Follow-up"),
    ("report_review", "Report review"),
    ("other", "Other"),
]

STATUS_CHOICES = [
        ("requested", "Requested"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
    ]

class MeetingRequest(Audit):
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name="meeting_requests")
    calendar = models.ForeignKey("Calendar", on_delete=models.CASCADE, related_name="meeting_requests")
    slot = models.OneToOneField(CalendarSlot, on_delete=models.PROTECT, related_name="booking")
    meeting_type = models.CharField(max_length=50, choices=MEETING_TYPE_CHOICES, default="first_meeting")
    preferred_slots = models.JSONField(default=list, blank=True)
    chosen_slot = models.DateTimeField(null=True, blank=True)
    agenda = models.TextField(blank=True)
    note = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="confirmed")
    processed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="processed_meeting_requests")
    processed_at = models.DateTimeField(null=True, blank=True)
    event = models.ForeignKey("Event", null=True, blank=True, on_delete=models.SET_NULL, related_name="meeting_request")
    cancelled_at = models.DateTimeField(null=True, blank=True)

    def cancel(self):
        self.status = "cancelled"
        self.cancelled_at = timezone.now()
        self.save()
        self.slot.is_available = True
        self.slot.save()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"MeetingRequest {self.pk} by {self.requester}"