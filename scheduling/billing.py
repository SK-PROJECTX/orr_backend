

from celery import shared_task
import stripe
from django.conf import settings
import time
from admin_portal.models import Meeting
stripe.api_key = settings.STRIPE_SECRET_KEY

@shared_task(bind=True, max_retries=3, default_retry_delay=5)
def charge_for_meeting(self, meeting_id):
    try:
        meeting = Meeting.objects.get(id=meeting_id)
        subscription = meeting.client.user.subscription
        plan = subscription.plan

        if plan.billing_type != "metered":
            return

        hours_used = meeting.duration_hours
        if hours_used <= 0:
            return

    
        subscription_item_id = subscription.stripe_subscription_item_id
        if not subscription_item_id:
            raise ValueError("Missing subscription_item_id — cannot report usage")

   
        usage_record = stripe.SubscriptionItem.usage_records.create(
            subscription_item=subscription_item_id,
            quantity=hours_used,
            timestamp=int(time.time()),
            action="increment"
        )

    
        subscription.used_hours = (subscription.used_hours or 0) + hours_used
        subscription.save()

        return usage_record
    except Exception as e:
        self.retry(exc=e)

