class BaseChannel:
    """Abstract base for notification channels."""

    def send(self, user, title, message, metadata=None):
        raise NotImplementedError("send() must be implemented by subclasses.")
