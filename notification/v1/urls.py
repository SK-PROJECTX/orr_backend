from django.urls import path

from .views import NotificationListView, NotificationUpdateView

urlpatterns = [
    path("notifications/", NotificationListView.as_view(), name="notifications-list"),
    path(
        "notifications/<int:notification_id>/",
        NotificationUpdateView.as_view(),
        name="notifications-update",
    ),
]
