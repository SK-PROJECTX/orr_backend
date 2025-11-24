from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MeetingRequestViewSet, MyCalendarView, CalendarMonthView

router = DefaultRouter()
router.register(r"meeting-requests", MeetingRequestViewSet, basename="meetingrequest")

urlpatterns = [
    path("mycalender", MyCalendarView.as_view(), name="mycalender"),
    path("calendar/<int:calendar_id>/month/", CalendarMonthView.as_view()),
]

urlpatterns += router.urls