from .channels.email_channel import EmailChannel
from .channels.inapp_channel import InAppChannel
from .channels.push_channel import  PushChannel


class NotificationService:
    """Centralized notification service layer."""

    def __init__(self):
        self.channels = {
            "email": EmailChannel(),
            "inapp": InAppChannel(),
            "push": PushChannel(),
        }

    def send_notification(self, user, title, message, channels=None, metadata=None):
        metadata = metadata or {}
        channels = channels or ["inapp"]

        for channel in channels:
            if channel in self.channels:
                self.channels[channel].send(user, title, message, metadata)
