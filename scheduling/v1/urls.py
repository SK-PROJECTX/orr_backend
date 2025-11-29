from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CalendarMonthView,
    MeetingRequestViewSet,
    MyCalendarView,
    UpdateMeetingPrepView,
)

router = DefaultRouter()
router.register(r"meeting-requests", MeetingRequestViewSet, basename="meetingrequest")

urlpatterns = [
    path("mycalender", MyCalendarView.as_view(), name="mycalender"),
    path("calendar/<int:calendar_id>/month/", CalendarMonthView.as_view()),
    path("meeting-preform", UpdateMeetingPrepView.as_view(), name="meeting-preform"),
]

urlpatterns += router.urls
