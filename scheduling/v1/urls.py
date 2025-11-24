from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MeetingRequestViewSet, MyCalendarView

router = DefaultRouter()
router.register(r"meeting-requests", MeetingRequestViewSet, basename="meetingrequest")

urlpatterns = [
    path("mycalender", MyCalendarView.as_view(), name="mycalender"),
]

urlpatterns += router.urls