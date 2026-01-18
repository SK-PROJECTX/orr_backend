from celery import shared_task
import stripe
from django.conf import settings
from django.db import transaction
from admin_portal.models import Meeting
import uuid
from notification.utils import notify_user

stripe.api_key = settings.STRIPE_SECRET_KEY

@shared_task(bind=True, max_retries=3, default_retry_delay=5)
def charge_for_meeting(self, meeting_id):
    try:
        meeting = Meeting.objects.get(id=meeting_id)
        subscription = meeting.client.user.subscription
        plan = subscription.plan
        client_user = meeting.client.user

        if plan.billing_type != "metered":
            return "Skipped: Not a metered plan."

        hours_used = meeting.duration_hours
        if hours_used <= 0:
            return "Skipped: Invalid duration."
            
       
        customer_id = meeting.client.user.stripe_customer_id
        if not customer_id:
            raise ValueError(f"User {meeting.client.user.id} has no Stripe Customer ID.")

        # 3. IDEMPOTENCY KEY (Crucial for Senior Devs)
        # Prevents double billing if this task accidentally runs twice.
        # We combine 'meeting_charge' + meeting_id to make it unique.
        idempotency_key = f"meeting_charge_{meeting.id}"

        
        stripe.InvoiceItem.create(
            customer=customer_id,
            price=plan.stripe_price_id, 
            quantity=hours_used,
            description=f"Immediate Charge for Meeting #{meeting.id}",
            subscription=subscription.stripe_subscription_id, 
            idempotency_key=f"{idempotency_key}_item" 
        )

        invoice = stripe.Invoice.create(
            customer=customer_id,
            subscription=subscription.stripe_subscription_id, 
            auto_advance=True, # Auto-finalize this invoice
            description=f"Charge for Meeting {meeting.id}",
            idempotency_key=f"{idempotency_key}_invoice" # Unique key for invoice creation
        )

        # Step C: Force Payment (If auto_advance doesn't trigger fast enough)
        invoice = stripe.Invoice.finalize_invoice(invoice.id)
        
        # Attempt to pay. If card fails, this raises a stripe.error.CardError
        paid_invoice = stripe.Invoice.pay(invoice.id)
        amount_paid = paid_invoice.amount_paid / 100

        # Only update our local DB if the Stripe payment actually succeeded.
        with transaction.atomic():
            subscription.used_hours = (subscription.used_hours or 0) + hours_used
            subscription.save()

            notify_user(
            client_user,
            "Payment Successful",
            f"We successfully charged ${amount_paid} for your recent meeting.",
            ["inapp", "email"], 
            {
                "type": "payment_success",
                # You must create this HTML template in your templates folder!
                "template": "payment/payment_success.html", 
                "context": {
                    "amount": amount_paid,
                    "meeting_id": meeting.ticket_id, # or meeting.id
                    "date": meeting.start_time, 
                    "invoice_url": paid_invoice.hosted_invoice_url, # Useful link for the user!
                    "client_name": client_user.first_name
                }
            }
        )
            

        return f"Success: Charged ${paid_invoice.amount_paid / 100} on Invoice {paid_invoice.id}"

    except stripe.error.CardError as e:
        # The card was declined. Don't retry blindly, notify the user/admin.
        # Log this specific error or trigger a 'payment_failed' email task.

        notify_user(
            meeting.client.user,
            "Payment Failed: Action Required",
            f"Your payment for the recent meeting failed. Please update your card.",
            ["inapp", "email"],
            {
                "type": "payment_failed",
                "template": "payment/payment_failed.html",
                "context": {
                    "reason": e.user_message,
                    "meeting_id": meeting.ticket_id,
                    "client_name": meeting.client.user.first_name,
                }
            }
        )
        print(f"Payment Declined for Meeting {meeting_id}: {e}")
        return f"Failed: Card Declined - {e.user_message}"

    except Exception as e:
        # For network errors or other crashes, we retry.
        # Idempotency keys above protect us from double-charging during retries.
        self.retry(exc=e)