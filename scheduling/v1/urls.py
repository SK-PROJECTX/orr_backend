from django.urls import include, path
from rest_framework.routers import DefaultRouter 

from .views import (
    CalendarMonthView,
    MyCalendarView,
    UpdateMeetingPrepView,
    CreateMeetingView,
    AvailableSlotsView,
    EventTypesView,
    MeetingChangeStatusView,
    MyMeetingsView,
    CalendarView
)


urlpatterns = [
    path('mymeetings', MyMeetingsView.as_view(), name='my-meeting'),
    path('meetings/<int:pk>/change-status/', MeetingChangeStatusView.as_view(), name='meeting-change-status'),
    path("mycalender", MyCalendarView.as_view(), name="mycalender"),
    path("calendar/<int:calendar_id>/month/", CalendarMonthView.as_view()),
    path("meeting-preform", UpdateMeetingPrepView.as_view(), name="meeting-preform"),
    path("meeting-slots/", AvailableSlotsView.as_view()),
    path("create-meeting/", CreateMeetingView.as_view()),
    path("event-type/", EventTypesView.as_view()),
    path("calendar/", CalendarView.as_view(), name="calendar-month"),
]
