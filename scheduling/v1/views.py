from calendar import monthrange
from datetime import date, timedelta
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime, timedelta
from services.meetings.calendly import CalendlyAPI
from .serializers import MeetingRequestSerializer, MeetingSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from rest_framework.decorators import action
from client.models import Activity

from ..models import Calendar, Event, MeetingRequest
from .serializers import (
    CalendarSerializer,
    EventSerializer,
    MeetingPrepSerializer,
    MeetingStatusChangeSerializer
)
import requests
from django.conf import settings
import logging
from services.meetings.calendly import CalendlyAPI

logger = logging.getLogger(__name__)
from admin_portal.models import Client,Meeting




class MyCalendarView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        calendar, created = Calendar.objects.get_or_create(
            owner_user=request.user,
            defaults={"name": f"{request.user.username}'s Calendar"},
        )
        serializer = CalendarSerializer(calendar)
        return Response(serializer.data)


@extend_schema(tags=["shedulling"])
class CalendarMonthView(APIView):
    permission_classes = [IsAuthenticated]
    serilizer_class = EventSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="year", type=int, location=OpenApiParameter.QUERY, required=True
            ),
            OpenApiParameter(
                name="month", type=int, location=OpenApiParameter.QUERY, required=True
            ),
        ],
        responses={200: dict},
    )
    def get(self, request, calendar_id):
        year = int(request.GET.get("year"))
        month = int(request.GET.get("month"))

        start_date = date(year, month, 1)
        last_day = monthrange(year, month)[1]
        end_date = date(year, month, last_day)

        events = Event.objects.filter(calendar_id=calendar_id).filter(
            Q(start__date__lte=end_date) & Q(end__date__gte=start_date)
        )

        days_data = []
        current = start_date
        while current <= end_date:
            day_events = [
                e for e in events if e.start.date() <= current <= e.end.date()
            ]
            days_data.append(
                {"date": current, "events": EventSerializer(day_events, many=True).data}
            )
            current += timedelta(days=1)

        return Response(
            {
                "calendar_id": calendar_id,
                "year": year,
                "month": month,
                "days": days_data,
            }
        )


class UpdateMeetingPrepView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MeetingPrepSerializer

    def patch(self, request, pk):
        meeting_request = get_object_or_404(
            MeetingRequest, pk=pk, requester=request.user
        )

        serializer = MeetingPrepSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        meeting_request.basic_context = data["basic_context"]
        meeting_request.goals = data["goals"]
        meeting_request.pain_points = data["pain_points"]
        meeting_request.save()

        Activity.objects.create(
            user=request.user,
            activity_type="Meeting Activity",
            title="Completed first meeting preparation",
            description="User submitted their meeting preparation details.",
            metadata={"meeting_request_id": meeting_request.id},
        )

        return Response({"message": "Meeting preparation updated successfully."})


@extend_schema(tags=["shedulling"])
class EventTypesView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        calendly = CalendlyAPI()
        event_types = calendly.get_event_types()  
        data = [
            {"name": et["name"], "uri": et["uri"]} for et in event_types["collection"]
        ]
        return Response(data)



@extend_schema(
        tags=["shedulling"],
        parameters=[
            OpenApiParameter(
                name="event_type_uri",
                type=str,
                required=True,
                description="Full Calendly event_type URL (e.g., https://api.calendly.com/event_types/XXXX)"
            )
        ]
    )
class AvailableSlotsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        meeting_type_uri = request.query_params.get("event_type_uri")
        start = datetime.now() + timedelta(hours=1)
        end = start + timedelta(days=7)

        calendly = CalendlyAPI()
        slots = calendly.get_available_slots(meeting_type_uri, start, end)

        return Response(slots)

@extend_schema(tags=["shedulling"])
class CreateMeetingView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MeetingRequestSerializer

    def post(self, request):
        serializer = MeetingRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        client = Client.objects.get(user=user)
        meeting = serializer.save(client=client)

        return Response(MeetingSerializer(meeting).data)
    




@extend_schema(
    tags=["shedulling"],
)
class MeetingChangeStatusView(APIView):
    """
    Endpoint to change the status of a meeting.
    POST /api/meetings/<pk>/change-status/
    """
    permission_classes = [IsAuthenticated]
    serializer_class = MeetingStatusChangeSerializer
    def post(self, request, pk):
        meeting = get_object_or_404(Meeting, pk=pk)
        new_status = request.data.get("status")
        user = request.user
        client = Client.objects.get(user=user)
        if meeting.client != client:
            raise PermissionDenied("You are not allowed to modify this meeting.")
        if new_status not in dict(Meeting.STATUS_CHOICES):
            return Response(
                {"error": "Invalid status", "allowed": dict(Meeting.STATUS_CHOICES)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        old_status = meeting.status
        meeting.status = new_status

        calendly = CalendlyAPI()

        try:
            if new_status == "cancelled" and meeting.calendar_event_id:
                calendly.cancel_event(meeting.calendar_event_id, reason=f"Status changed to {new_status} via portal")

            elif new_status == "rescheduled" and meeting.calendar_event_id:
                pass 
            elif new_status == "confirmed" and old_status == "requested":
                if not meeting.calendar_event_id:
                    calendly_data = calendly.schedule_event(meeting)
                    meeting.calendar_event_id = calendly_data["event_uuid"]
                    meeting.meeting_link = calendly_data["invite_link"]
                    meeting.confirmed_datetime = meeting.requested_datetime

        except Exception as e:
            meeting.internal_notes += f"\n[Auto] Calendly sync warning ({new_status}): {str(e)}"
            logger.warning(f"Calendly sync failed for meeting {meeting.id}: {e}")

        meeting.save()
        valid_statuses = dict(Meeting.STATUS_CHOICES)

        old_status_display = valid_statuses[old_status]
        new_status_display = valid_statuses[new_status]
        return Response({
            "id": meeting.id,
            "status": new_status,
            "status_display": new_status_display,
            "message": f"Status changed from {old_status_display} → {new_status_display}",
        }, status=status.HTTP_200_OK)
        
@extend_schema(
    tags=["shedulling"],
    description="Get all meetings created by the authenticated client.",
    responses=MeetingSerializer(many=True),
)
class MyMeetingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        client = Client.objects.get(user=user)
        meetings = Meeting.objects.filter(client=client).order_by("-id")
        serializer = MeetingSerializer(meetings, many=True)
        return Response(serializer.data)