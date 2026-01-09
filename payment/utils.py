
import stripe
from django.conf import settings
from .models import StripeCustomer
import stripe
from django.conf import settings



stripe.api_key = settings.STRIPE_SECRET_KEY


def get_or_create_stripe_customer(user):
    stripe_profile, created = StripeCustomer.objects.get_or_create(user=user)

    if stripe_profile.stripe_customer_id:
        return stripe_profile

    customer = stripe.Customer.create(
        email=user.email,
        name=user.get_full_name() or user.username,
        metadata={"user_id": user.id},
    )

    stripe_profile.stripe_customer_id = customer.id
    stripe_profile.save(update_fields=["stripe_customer_id"])

    return stripe_profile





