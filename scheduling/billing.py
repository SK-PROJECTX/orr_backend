import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def charge_for_meeting(meeting):
    subscription = meeting.client.user.subscription
    plan = subscription.plan

    if plan.billing_type != "metered":
        return  

    hours_used = meeting.duration_hours  
    if hours_used <= 0:
        return

    # Calculate amount in cents
    hourly_rate_cents = plan.amount 
    amount_cents = int(hours_used * hourly_rate_cents)


    charge = stripe.Charge.create(
        amount=amount_cents,
        currency="usd",
        customer=subscription.stripe_customer_id,
        description=f"Meeting charge ({hours_used:.2f} hours)",
    )

    # Save usage history
    subscription.used_hours = (subscription.used_hours or 0) + hours_used
    subscription.save()

    return charge
