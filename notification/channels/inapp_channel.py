from ..models import Notification
from .base_channel import BaseChannel


class InAppChannel(BaseChannel):
    def send(self, user, title, message, metadata=None):
        Notification.objects.create(
            user=user,
            title=title,
            message=message,
        )
