from django.utils import timezone
from django.db import transaction
from ...notification.utils import notify_user  
from django.contrib.auth import get_user_model

User = get_user_model()


def deactivate_subscription(subscription, reason: str):
    """
    Centralized subscription deactivation logic.
    Safe to call multiple times (idempotent).
    """
    if not subscription.is_active:
        return False

    with transaction.atomic():
        subscription.is_active = False
        subscription.save(update_fields=["is_active"])

    user = subscription.user

    notify_user(
        user,
        "Subscription Ended",
        f"Your {subscription.plan_name} subscription has ended",
        ["inapp", "email"],
        {
            "type": "subscription",
            "template": "subscriptions/subscription_ended.html",
            "context": {
                "plan_name": subscription.plan_name,
                "ended_at": timezone.now(),
                "reason": reason,
            },
        },
    )


    return True
