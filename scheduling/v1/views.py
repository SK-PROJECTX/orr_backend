from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import MeetingRequestCreateSerializer, CalendarSerializer, EventSerializer
from ..models import MeetingRequest, Calendar, Event
from ..utils import slot_conflicts
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils import timezone
from django.db.models import Q
from datetime import date, timedelta
from calendar import monthrange
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter

@extend_schema(tags=["shedulling"])
class MeetingRequestViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = MeetingRequestCreateSerializer
    queryset = MeetingRequest.objects.all()

    def create(self, request, *args, **kwargs):
        """
        Endpoint to submit meeting request from the calendar UI.
        Expected payload (JSON):
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        calendar = get_object_or_404(Calendar, pk=data["calendar"])
        duration_minutes = request.data.get("duration_minutes", 60)
        free_slots = []
        busy_slots = []
        for dt in data["preferred_slots"]:
            has_conflict = slot_conflicts(calendar.id, dt, duration_minutes=duration_minutes)
            if not has_conflict:
                free_slots.append(dt.isoformat())
            else:
                busy_slots.append(dt.isoformat())
        mr = MeetingRequest.objects.create(
            requester=request.user,
            calendar=calendar,
            meeting_type=data["meeting_type"],
            preferred_slots=[d.isoformat() for d in data["preferred_slots"]],
            agenda=data.get("agenda", ""),
            note=data.get("note", ""),
            status="requested",
        )

        return Response({
            "message": "Meeting request created",
            "meeting_request_id": mr.id,
            "free_slots": free_slots,
            "busy_slots": busy_slots,
            "status": mr.status
        }, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"], url_path="confirm")
    def confirm(self, request, pk=None):
        """
        Admin or owner confirms a request and schedules an Event.
        Payload (optional): {"chosen_slot": "2025-09-18T17:30:00+01:00", "duration_minutes": 60}
        """
        mr = self.get_object()
        cal = mr.calendar
        if not (request.user.is_staff or (hasattr(cal, "owner_user") and cal.owner_user == request.user)):
            return Response({"detail": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)

        chosen_iso = request.data.get("chosen_slot")
        from django.utils.dateparse import parse_datetime
        chosen_dt = parse_datetime(chosen_iso) if chosen_iso else None
        if chosen_dt is None:
            duration_minutes = request.data.get("duration_minutes", 60)
            picked = None
            for s_iso in mr.preferred_slots:
                s_dt = parse_datetime(s_iso)
                if not slot_conflicts(cal.id, s_dt, duration_minutes):
                    picked = s_dt
                    break
            if not picked:
                return Response({"detail": "No available preferred slots"}, status=status.HTTP_400_BAD_REQUEST)
            chosen_dt = picked
            duration_minutes = request.data.get("duration_minutes", 60)
        else:
            duration_minutes = request.data.get("duration_minutes", 60)
            if slot_conflicts(cal.id, chosen_dt, duration_minutes):
                return Response({"detail": "Chosen slot conflicts"}, status=status.HTTP_400_BAD_REQUEST)
        from ..models import Event
        end_dt = chosen_dt + timezone.timedelta(minutes=duration_minutes)
        event = Event.objects.create(
            calendar=cal,
            title=f"{mr.get_meeting_type_display()} with {mr.requester.get_full_name() or mr.requester.username}",
            description=mr.agenda,
            start=chosen_dt,
            end=end_dt,
            created_by=request.user
        )
        event.attendees.add(mr.requester)

        mr.chosen_slot = chosen_dt
        mr.event = event
        mr.status = "confirmed"
        mr.processed_by = request.user
        mr.processed_at = timezone.now()
        mr.save()


        return Response({"message": "Meeting confirmed", "event_id": event.id}, status=status.HTTP_200_OK)
    
class MyCalendarView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        calendar, created = Calendar.objects.get_or_create(
            owner_user=request.user,
            defaults={"name": f"{request.user.username}'s Calendar"}
        )
        serializer = CalendarSerializer(calendar)
        return Response(serializer.data)




@extend_schema(tags=["shedulling"])
class CalendarMonthView(APIView):
    permission_classes = [IsAuthenticated]
    serilizer_class= EventSerializer
    @extend_schema(
        parameters=[
            OpenApiParameter(name="year", type=int, location=OpenApiParameter.QUERY, required=True),
            OpenApiParameter(name="month", type=int, location=OpenApiParameter.QUERY, required=True),
        ],
        responses={200: dict}
    )
    def get(self, request, calendar_id):
        year = int(request.GET.get("year"))
        month = int(request.GET.get("month"))

        start_date = date(year, month, 1)
        last_day = monthrange(year, month)[1]
        end_date = date(year, month, last_day)

        events = Event.objects.filter(
            calendar_id=calendar_id
        ).filter(
            Q(start__date__lte=end_date) &
            Q(end__date__gte=start_date)
        )

        days_data = []
        current = start_date
        while current <= end_date:
            day_events = [
                e for e in events
                if e.start.date() <= current <= e.end.date()
            ]
            days_data.append({
                "date": current,
                "events": EventSerializer(day_events, many=True).data
            })
            current += timedelta(days=1)

        return Response({
            "calendar_id": calendar_id,
            "year": year,
            "month": month,
            "days": days_data
        })