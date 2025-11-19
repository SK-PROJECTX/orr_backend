import logging

from .dispatcher import NotificationService

logger = logging.getLogger(__name__)


def notify_user(user, title, message, channels=None, metadata=None):
    try:
        NotificationService().send_notification(
            user, title, message, channels, metadata
        )
        logger.info(
            f"Notification sent successfully to {user} via {channels or ['inapp']}"
        )
    except Exception as e:
        logger.exception(f" Failed to send notification to {user}: {e}")
        raise