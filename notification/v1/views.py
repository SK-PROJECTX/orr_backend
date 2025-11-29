from rest_framework import generics, permissions
from rest_framework.response import Response

from ..models import Notification
from .serializers import NotificationSerializer


class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)


class NotificationUpdateView(generics.UpdateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = "notification_id"

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    def patch(self, request, *args, **kwargs):
        notification = self.get_object()
        is_read = request.data.get("is_read")

        if is_read is None:
            return Response({"error": "is_read field is required"}, status=400)

        notification.is_read = bool(is_read)
        notification.save()

        return Response(
            {"message": "Notification updated", "is_read": notification.is_read},
            status=status.HTTP_200_OK,
        )
