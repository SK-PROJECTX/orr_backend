from celery import shared_task
from celery.utils.log import get_task_logger
from datetime import datetime
from decimal import Decimal
from django.db import transaction
from django.utils.timezone import make_aware
import stripe

from .models import User, PricingPlan, Subscription, CheckoutSessionLog, Invoice
from admin_portal.payment_ticket_service import PaymentTicketService

logger = get_task_logger(__name__)


@shared_task(bind=True, max_retries=10, default_retry_delay=5)
def handle_stripe_event(self, event: dict):
    """
    Unified handler for all Stripe webhooks.
    Ensures idempotency, race-condition recovery, and safe DB operations.
    """
    event_type = event.get("type")
    data = event.get("data", {}).get("object", {}) or {}
    session_id = data.get("id") if "session" in event_type else None

    logger.info("Received Stripe event: %s", event_type)

    try:

        if event_type == "checkout.session.completed":

            if session_id:
                CheckoutSessionLog.objects.filter(stripe_session_id=session_id).update(status="completed")

            metadata = data.get("metadata") or {}
            user_id = metadata.get("user_id")
            plan_id = metadata.get("plan_id")
            billing_type = metadata.get("billing_type")
            customer_id = data.get("customer")
            subscription_id = data.get("subscription")

            logger.info(
                "checkout.session.completed | user=%s plan=%s sub=%s customer=%s",
                user_id, plan_id, subscription_id, customer_id
            )

            if not subscription_id:
                logger.error("checkout.session.completed missing subscription_id")
                return

           
            try:
                user = User.objects.get(id=int(user_id))
            except Exception:
                logger.error("Invalid or missing user_id in metadata: %s", user_id)
                return

            try:
                plan = PricingPlan.objects.get(id=int(plan_id))
            except Exception:
                logger.error("Invalid or missing plan_id in metadata: %s", plan_id)
                plan = None

            # Fetch Stripe subscription
            try:
                sub = stripe.Subscription.retrieve(subscription_id)
                period_end = sub.get("current_period_end")
                current_period_end = make_aware(datetime.fromtimestamp(period_end)) if period_end else None

                item = sub.get("items", {}).get("data", [{}])[0]
                plan_name = item.get("price", {}).get("nickname") or item.get("plan", {}).get("nickname") or "Unknown Plan"
                subscription_item_id = item["id"]
            except Exception:
                logger.exception("Failed retrieving subscription %s", subscription_id)
                return

            # Save subscription
            try:
                Subscription.objects.update_or_create(
                    user=user,
                    defaults={
                        "stripe_subscription_id": subscription_id,
                        "stripe_customer_id": customer_id,
                        "plan": plan,
                        "plan_name": plan_name,
                        "stripe_subscription_item_id": subscription_item_id,
                        "is_active": True,
                        "current_period_end": current_period_end,
                        "used_hours": 0 if billing_type == "metered" else None,
                    }
                )
                logger.info("Subscription saved: user=%s subscription=%s", user.id, subscription_id)

            except Exception:
                logger.exception("Error saving local subscription")
            
            return

      
        if event_type in ("invoice.finalized", "invoice.paid", "invoice.payment_succeeded"):

            invoice_id = data.get("id")
            customer_id = data.get("customer")

            logger.info("Handling invoice event %s | invoice=%s", event_type, invoice_id)

            if not invoice_id or not customer_id:
                logger.error("Invoice event missing invoice_id or customer_id")
                return

            # Ensure subscription exists first (race condition fix)
            try:
                subscription = Subscription.objects.filter(
                    stripe_customer_id=customer_id
                ).first()

                if not subscription:
                    logger.warning(
                        "Invoice %s arrived before subscription exists (customer=%s). Skipping.",
                        invoice_id,
                        customer_id,
                    )
                    return 

                user = subscription.user

            except Subscription.DoesNotExist as exc:
                raise self.retry(exc=exc, countdown=5)

            # Extract invoice details
            try:
                amount_cents = int(data.get("amount_due") or data.get("total") or 0)
                amount = Decimal(amount_cents) / Decimal(100)

                created_ts = data.get("created")
                billing_date = (
                    make_aware(datetime.fromtimestamp(created_ts)).date()
                    if created_ts else None
                )

                line = data.get("lines", {}).get("data", [{}])[0]
                description = (
                    line.get("description")
                    or line.get("plan", {}).get("nickname")
                    or "Subscription"
                )

                billing_title = f"Invoice for {description}"
                plan_name = description

                invoice_pdf = data.get("invoice_pdf") or data.get("invoice_pdf_url")
                hosted_invoice_url = data.get("hosted_invoice_url")
                currency = (data.get("currency") or "").upper()

                # Idempotent save — prevents duplicate inserts
                with transaction.atomic():
                    Invoice.objects.update_or_create(
                        stripe_invoice_id=invoice_id,
                        defaults={
                            "user": user,
                            "billing_title": billing_title,
                            "status": data.get("status"),
                            "billing_date": billing_date,
                            "amount": amount,
                            "currency": currency,
                            "plan": plan_name,
                            "invoice_pdf": invoice_pdf,
                            "hosted_invoice_url": hosted_invoice_url,
                            "users": 1,
                        },
                    )

                logger.info("Invoice saved: %s for user %s", invoice_id, user.id)

            except Exception:
                logger.exception("Failed saving invoice %s", invoice_id)

            return
        if event_type in ("checkout.session.expired", "checkout.session.async_payment_failed"):
            if session_id:
                CheckoutSessionLog.objects.filter(stripe_session_id=session_id).update(status="expired")
            return
        if event["type"] == "setup_intent.succeeded":
            intent = event["data"]["object"]
            customer_id = intent["customer"]
            payment_method_id = intent["payment_method"]

            subscription = Subscription.objects.filter(
                stripe_customer_id=customer_id
            ).first()

            if subscription:
                subscription.default_payment_method = payment_method_id
                subscription.save()

                stripe.Customer.modify(
                    customer_id,
                    invoice_settings={"default_payment_method": payment_method_id}
                )
        if event_type == "customer.subscription.deleted":
            sub_id = data.get("id")
            if not sub_id:
                logger.error("subscription.deleted missing id")
                return

            try:
                subscription = Subscription.objects.get(stripe_subscription_id=sub_id)
                PaymentTicketService.create_subscription_cancelled_ticket(subscription)
                subscription.is_active = False
                subscription.save()
                logger.info("Subscription marked inactive: %s", sub_id)
            except Subscription.DoesNotExist as exc:
                logger.warning("Subscription not found for deleted Stripe ID %s", sub_id)
                raise self.retry(exc=exc, countdown=5)

            return

        logger.debug("Unhandled Stripe event type: %s", event_type)

    except Exception as exc:
        logger.exception("Unhandled error processing %s", event_type)
        raise self.retry(exc=exc, countdown=5)
