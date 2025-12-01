from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CalendarMonthView,
    MeetingRequestViewSet,
    MyCalendarView,
    UpdateMeetingPrepView,
    CreateMeetingView,
    AvailableSlotsView,
    EventTypesView,
)

router = DefaultRouter()
router.register(r"meeting-requests", MeetingRequestViewSet, basename="meetingrequest")

urlpatterns = [
    path("mycalender", MyCalendarView.as_view(), name="mycalender"),
    path("calendar/<int:calendar_id>/month/", CalendarMonthView.as_view()),
    path("meeting-preform", UpdateMeetingPrepView.as_view(), name="meeting-preform"),
    path("meeting-slots/", AvailableSlotsView.as_view()),
    path("create-meeting/", CreateMeetingView.as_view()),
    path("event-type/", EventTypesView.as_view()),
]

urlpatterns += router.urls
