
import stripe
from django.conf import settings
from .models import StripeCustomer
import stripe
from django.conf import settings



stripe.api_key = settings.STRIPE_SECRET_KEY


def get_or_create_stripe_customer(user):
    try:
        return user.stripe_profile.stripe_customer_id
    except StripeCustomer.DoesNotExist:
        customer = stripe.Customer.create(
            email=user.email,
            name=user.get_full_name() or user.username,
            metadata={"user_id": user.id},
        )

        StripeCustomer.objects.create(
            user=user,
            stripe_customer_id=customer.id
        )

        return customer.id




class StripeSubscriptionService:

    @staticmethod
    def has_active_subscription(stripe_customer_id: str) -> bool:
        subscriptions = stripe.Subscription.list(
            customer=stripe_customer_id,
            status="all",
            limit=10
        )

        for sub in subscriptions.data:
            if sub.status in ("active", "trialing"):
                return True

        return False
