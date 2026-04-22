from celery import shared_task
from celery.utils.log import get_task_logger
from datetime import datetime
from decimal import Decimal
from django.db import transaction
from django.utils.timezone import make_aware
from django.utils import timezone
import stripe

from .models import (
    User,
    PricingPlan,
    Subscription,
    CheckoutSessionLog,
    Invoice,
    StripeEvent,
    StripeCustomer,
)
from client.models import Wallet, Transaction
from admin_portal.payment_ticket_service import PaymentTicketService
from django.db import IntegrityError

logger = get_task_logger(__name__)


@shared_task(bind=True, max_retries=4, default_retry_delay=10)
def handle_stripe_event(self, event: dict):
    """
    Unified Stripe webhook handler with strict idempotency and retry safety.
    """

    event_id = event.get("id")
    event_type = event.get("type")

    if not event_id or not event_type:
        logger.error("Stripe event missing id or type")
        return

    data = event.get("data", {}).get("object", {}) or {}
    session_id = data.get("id") if event_type.startswith("checkout.session") else None

    logger.info("Processing Stripe event: %s", event_type)

    with transaction.atomic():
        try:
            with transaction.atomic():
                StripeEvent.objects.create(
                    event_id=event_id,
                    event_type=event_type,
                )
        except IntegrityError:
            logger.info("Duplicate Stripe event ignored: %s", event_id)
            return


        try:
            # -------------------------------
            # CHECKOUT COMPLETED
            # -------------------------------
            if event_type == "checkout.session.completed":
                if session_id:
                    CheckoutSessionLog.objects.filter(
                        stripe_session_id=session_id
                    ).update(status="completed")

                metadata = data.get("metadata") or {}
                user_id = metadata.get("user_id")
                plan_id = metadata.get("plan_id")
                billing_type = metadata.get("billing_type")

                subscription_id = data.get("subscription")
                customer_id = data.get("customer")

                if not (user_id and subscription_id):
                    logger.error("checkout.session.completed missing metadata")
                    raise ValueError("Missing metadata")

                user = User.objects.get(id=int(user_id))
                
                # Check if it's a Wallet Top-up
                if metadata.get('type') == 'top_up':
                    # Use session_id as reference_id for idempotency
                    if Transaction.objects.filter(reference_id=session_id).exists():
                        logger.info("Top-up transaction already processed for session: %s", session_id)
                        return
                        
                    amount = Decimal(metadata.get('amount', 0))
                    wallet, created = Wallet.objects.get_or_create(owner=user)
                    
                    Transaction.objects.create(
                        wallet=wallet,
                        amount=amount,
                        transaction_type='payment',
                        description="Wallet Top-up via Stripe Checkout",
                        reference_id=session_id
                    )
                    logger.info("Wallet credited for user %s: %s", user.id, amount)
                    return

                plan = PricingPlan.objects.filter(id=int(plan_id)).first()

                sub = stripe.Subscription.retrieve(subscription_id)
                period_end = sub.get("current_period_end")
                current_period_end = (
                    make_aware(datetime.fromtimestamp(period_end))
                    if period_end else None
                )

                item = sub["items"]["data"][0]
                subscription_item_id = item["id"]

                Subscription.objects.update_or_create(
                    user=user,
                    defaults={
                        "stripe_subscription_id": subscription_id,
                        "stripe_customer_id": customer_id,
                        "stripe_subscription_item_id": subscription_item_id,
                        "plan": plan,
                        "plan_name": plan.name if plan else "Unknown Plan",
                        "is_active": True,
                        "current_period_end": current_period_end,
                        "used_hours": 0 if billing_type == "metered" else None,
                    },
                )
                logger.info("Subscription activated: %s", subscription_id)
                return

            # -------------------------------
            # SUBSCRIPTION CREATED / UPDATED
            # -------------------------------
            if event_type in (
                "customer.subscription.created",
                "customer.subscription.updated",
            ):
                subscription_id = data.get("id")
                status = data.get("status")
                period_end = data.get("current_period_end")

                current_period_end = (
                    make_aware(datetime.fromtimestamp(period_end))
                    if period_end else None
                )

                is_active = status in ("active", "trialing")

                updated = Subscription.objects.filter(
                    stripe_subscription_id=subscription_id
                ).update(
                    is_active=is_active,
                    current_period_end=current_period_end,
                )

                if not updated:
                    logger.warning(
                        "Subscription %s not found yet, retrying", subscription_id
                    )
                    raise self.retry(countdown=10)
                return

            # -------------------------------
            # PAYMENT INTENT SUCCEEDED (Direct Top-ups)
            # -------------------------------
            if event_type == "payment_intent.succeeded":
                metadata = data.get("metadata") or {}
                if metadata.get('type') == 'top_up':
                    payment_intent_id = data.get("id")
                    user_id = metadata.get("user_id")
                    amount = Decimal(metadata.get("amount", 0))
                    
                    if not payment_intent_id or not user_id:
                        logger.error("payment_intent.succeeded top_up missing identifiers")
                        return

                    # Idempotency check
                    if Transaction.objects.filter(reference_id=payment_intent_id).exists():
                        logger.info("Top-up transaction already processed for intent: %s", payment_intent_id)
                        return

                    user = User.objects.get(id=int(user_id))
                    wallet, created = Wallet.objects.get_or_create(owner=user)
                    
                    Transaction.objects.create(
                        wallet=wallet,
                        amount=amount,
                        transaction_type='payment',
                        description="Wallet Top-up via Saved Card",
                        reference_id=payment_intent_id
                    )
                    logger.info("Wallet credited via Direct Payment for user %s: %s", user.id, amount)
                return

            # -------------------------------
            # INVOICE EVENTS
            # -------------------------------
            if event_type in (
                "invoice.paid",
                "invoice.payment_failed",
            ):
                normalized_event = "payment_succeeded" if event_type == "invoice.paid" else "payment_failed"

                invoice_id = data.get("id")
                customer_id = data.get("customer")
                subscription_id = (
                    data.get("subscription")
                    or data.get("lines", {})
                        .get("data", [{}])[0]
                        .get("subscription")
                )

                if not invoice_id or not subscription_id:
                    logger.error("Invoice event missing identifiers")
                    raise ValueError("Missing identifiers")

                if Invoice.objects.filter(stripe_invoice_id=invoice_id).exists():
                    logger.info("Duplicate invoice ignored: %s", invoice_id)
                    return

                subscription = Subscription.objects.filter(
                    stripe_subscription_id=subscription_id
                ).first()

                if not subscription:
                    raise self.retry(countdown=20, max_retries=4)
                stripe_profile = StripeCustomer.objects.filter(
                    stripe_customer_id=customer_id
                ).first()

                if not stripe_profile:
                    stripe_profile = StripeCustomer.objects.filter(user=subscription.user).first()
                    
                    if stripe_profile:
                        # 2. If found, UPDATE the existing profile with the new customer ID
                        stripe_profile.stripe_customer_id = customer_id
                        stripe_profile.save(update_fields=['stripe_customer_id'])
                    else:
                        stripe_profile = StripeCustomer.objects.create(
                            user=subscription.user,
                            stripe_customer_id=customer_id,
                            last_payment_failed=False,
                        )
                if normalized_event == "payment_succeeded":
                    subscription.is_active = True
                    stripe_profile.last_payment_failed = False

                elif normalized_event == "payment_failed":
                    subscription.is_active = False
                    stripe_profile.last_payment_failed = True

                subscription.save(update_fields=["is_active"])
                stripe_profile.save(update_fields=["last_payment_failed"])

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

                Invoice.objects.update_or_create(
                    stripe_invoice_id=invoice_id,
                    defaults={
                        "user": subscription.user,
                        "billing_title": f"Invoice for {description}",
                        "status": data.get("status"),
                        "billing_date": billing_date,
                        "amount": amount,
                        "currency": (data.get("currency") or "").upper(),
                        "plan": description,
                        "invoice_pdf": data.get("invoice_pdf"),
                        "hosted_invoice_url": data.get("hosted_invoice_url"),
                        "users": 1,
                    },
                )

                logger.info("Invoice processed: %s", invoice_id)
                return

            # -------------------------------
            # SETUP INTENT
            # -------------------------------
            if event_type == "setup_intent.succeeded":
                customer_id = data.get("customer")
                payment_method_id = data.get("payment_method")

                subscription = Subscription.objects.filter(
                    stripe_customer_id=customer_id
                ).first()

                if subscription:
                    subscription.default_payment_method = payment_method_id
                    subscription.save(update_fields=["default_payment_method"])

                    stripe.Customer.modify(
                        customer_id,
                        invoice_settings={
                            "default_payment_method": payment_method_id
                        },
                    )
                return

            # -------------------------------
            # SUBSCRIPTION DELETED
            # -------------------------------
            if event_type == "customer.subscription.deleted":
                subscription_id = data.get("id")

                subscription = Subscription.objects.filter(
                    stripe_subscription_id=subscription_id
                ).first()

                if not subscription:
                    return

                if subscription.is_active:
                    PaymentTicketService.create_subscription_cancelled_ticket(
                        subscription
                    )
                    subscription.is_active = False
                    subscription.save(update_fields=["is_active"])
                return

            logger.debug("Unhandled Stripe event type: %s", event_type)

        except Exception as exc:
            raise self.retry(exc=exc, countdown=10, max_retries=4)


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 3, "countdown": 30},
)
def deactivate_expired_subscriptions(self):
    now = timezone.now()

    subs = Subscription.objects.filter(
        is_active=True,
        current_period_end__isnull=False,
        current_period_end__lte=now,
    )

    count = 0
    for sub in subs.select_related("user"):
        from ..services.subscriptions.deactivate_sub import deactivate_subscription

        if deactivate_subscription(sub, reason="period_end_reached"):
            count += 1

    logger.info("Celery deactivated %s subscriptions", count)
    return count