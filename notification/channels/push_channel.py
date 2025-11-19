import logging

from .base_channel import BaseChannel

logger = logging.getLogger(__name__)


class PushChannel(BaseChannel):
    """Stub for mobile/web push notifications."""

    def send(self, user, title, message, metadata=None):
        logger.info(f"Push notification to {user}: {title}")
