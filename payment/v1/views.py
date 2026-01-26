from datetime import datetime
import stripe
from django.conf import settings
from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from common.permissions import IsAdminUser
from ..tasks import handle_stripe_event
from django.utils.timezone import make_aware
from ..models import Invoice, PricingPlan, Subscription, CheckoutSessionLog, StripeCustomer
from .serializers import (
    BillingPortalSerializer,
    SetupIntentResponseSerializer,
    ChangePlanSerializer,
    CreateCheckoutSerializer,
    InvoiceHistorySerializer,
    PauseSubscriptionSerializer,
    PricingPlanSerializer,
    AddPaymentMethodSerializer
)
from ..utils import get_or_create_stripe_customer
import logging
logger = logging.getLogger(__name__)
stripe.api_key = settings.STRIPE_SECRET_KEY  

User = settings.AUTH_USER_MODEL


@extend_schema(
    tags=["payment"],
)
class CreateCheckoutSession(APIView):
    serializer_class = CreateCheckoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        price_id = request.data.get("price_id")

        if not price_id:
            logger.error("price_id is missing in request data")
            return Response({"error": "price_id is required"}, status=400)
        
        try:
            plan = PricingPlan.objects.get(stripe_price_id=price_id)
        except PricingPlan.DoesNotExist:
            logger.error(f"PricingPlan not found for price_id: {price_id}")
            return Response({"error": "Invalid price_id"}, status=400)
        
        if Subscription.objects.filter(user=request.user, plan=plan, is_active=True).exists():
            return Response(
                {"error": "You already have an active subscription for this plan."},
                status=400
            )
        if plan.billing_type == "monthly":
            try:
                logger.info(f"Creating Stripe session for user: {request.user.id} with plan: {plan.id}")
                stripe_profile = get_or_create_stripe_customer(request.user)
                session = stripe.checkout.Session.create(
                    mode="subscription",
                    payment_method_types=["card"],
                    line_items=[{"price": price_id, "quantity": 1}],
                    customer_email=request.user.email,
                    metadata={
                        "user_id": request.user.id,
                        "plan_id": plan.id,
                        "billing_type": plan.billing_type,
                        "email": request.user.email,
                    },
                    success_url=settings.STRIPE_SUCCESS_URL
                    + "?session_id={CHECKOUT_SESSION_ID}",
                    cancel_url=settings.STRIPE_CANCEL_URL,
                )
                CheckoutSessionLog.objects.create(
                    user=request.user,
                    plan=plan,
                    stripe_session_id=session.id,
                    status="initiated" 
                )
                logger.info(f"Stripe session created successfully, session_id: {session.id}")
                return Response({"checkout_url": session.url})

            except Exception as e:
                logger.error(f"Error creating Stripe session: {str(e)}")
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        elif plan.billing_type == "metered":
            try:
                stripe_profile = getattr(request.user, "stripe_profile", None)

                if not stripe_profile or not stripe_profile.has_valid_payment_method:
                    return Response(
                        {"error": "Add a valid payment method before subscribing"},
                        status=403,
                    )

                stripe_profile = get_or_create_stripe_customer(request.user)
                customer_id = stripe_profile.stripe_customer_id

                subscription = stripe.Subscription.create(
                    customer=customer_id,
                    items=[{"price": price_id, "quantity": 1}],
                    expand=["latest_invoice.payment_intent"],
                    metadata={
                        "user_id": request.user.id,
                        "plan_id": plan.id,
                        "billing_type": plan.billing_type,
                    }
                )
                
                stripe_item_id = subscription["items"]["data"][0]["id"]

                Subscription.objects.update_or_create(
                    stripe_subscription_id=subscription.id,
                    defaults={
                        "user": request.user,
                        "stripe_customer_id": customer_id,
                        "plan": plan,
                        "plan_name": plan.name,
                        "stripe_subscription_item_id": stripe_item_id,
                        "is_active": True,
                        "used_hours": 0,
                    },
                )

                return Response(
                    {
                        "message": "Metered subscription created",
                        "subscription_id": subscription.id,
                    },
                    status=201,
                )
              
            except Exception as e:
                return Response({"error": str(e)}, status=400)
        else:
           return Response({"error": "Invalid billing type"}, status=400)


@csrf_exempt
def stripe_webhook(request):

    if request.method == "GET":
       return HttpResponse("pong", status=200)
    
    if request.method != "POST":
        return HttpResponse(status=405)
    
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    if not sig_header:
        logger.error("Missing Stripe signature header")
        return HttpResponse(status=400)

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
    except Exception as e:
        logger.exception("Invalid Stripe webhook signature")
        return HttpResponse(status=400)

    
    try:
        handle_stripe_event.delay(event)  
    except Exception:
        logger.exception("Failed to enqueue Stripe event to Celery")
    return HttpResponse(status=200)








@extend_schema(
    tags=["payment"],
)
class ChangePlanView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePlanSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        price_id = serializer.validated_data["price_id"]
        prorate = serializer.validated_data["prorate"]

        try:
            sub = request.user.subscription
        except Subscription.DoesNotExist:
            return Response({"detail": "No subscription"}, status=404)

        try:
            stripe_sub = stripe.Subscription.retrieve(sub.stripe_subscription_id)

            item_id = stripe_sub["items"]["data"][0]["id"]

            updated = stripe.Subscription.modify(
                sub.stripe_subscription_id,
                items=[
                    {
                        "id": item_id,
                        "price": price_id,
                    }
                ],
                proration_behavior="create_prorations" if prorate else "none",
            )

            sub.plan_name = (
                updated["items"]["data"][0]["plan"].get("nickname") or sub.plan_name
            )
            sub.current_period_end = timezone.datetime.fromtimestamp(
                updated["current_period_end"], tz=timezone.utc
            )
            sub.save()

            return Response({"stripe_subscription": updated})
        except Exception as e:
            return Response({"error": str(e)}, status=400)


@extend_schema(
    tags=["payment"],
)
class PauseSubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PauseSubscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            sub = request.user.subscription
        except Subscription.DoesNotExist:
            return Response({"detail": "No subscription"}, status=404)

        action = serializer.validated_data["action"]

        try:
            if action == "pause":
                body = {
                    "pause_collection": {
                        "behavior": serializer.validated_data.get(
                            "behavior", "keep_as_draft"
                        )
                    }
                }
                if "resumes_at" in serializer.validated_data:
                    resumes_at = serializer.validated_data["resumes_at"]
                    body["pause_collection"]["resumes_at"] = int(resumes_at.timestamp())
                updated = stripe.Subscription.modify(sub.stripe_subscription_id, **body)

                sub.is_active = False
                sub.save()
                return Response({"paused_subscription": updated})

            else:
                updated = stripe.Subscription.modify(
                    sub.stripe_subscription_id, pause_collection=""
                )
                sub.is_active = True
                sub.save()
                return Response({"resumed_subscription": updated})

        except Exception as e:
            return Response({"error": str(e)}, status=400)


@extend_schema(
    tags=["payment"],
)
class BillingPortalView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BillingPortalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            sub = request.user.subscription
        except Subscription.DoesNotExist:
            return Response({"detail": "No subscription"}, status=404)

        try:
            session = stripe.billing_portal.Session.create(
                customer=sub.stripe_customer_id,
                return_url=serializer.validated_data["return_url"],
            )
            return Response({"url": session.url})
        except Exception as e:
            return Response({"error": str(e)}, status=400)




@extend_schema(
    tags=["payment"],
)
class BillingHistoryView(ListAPIView):
    serializer_class = InvoiceHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Invoice.objects.filter(user=self.request.user).order_by("-created_at")


@extend_schema(
    tags=["payment"],
)
class PricingPlanViewSet(viewsets.ModelViewSet):
    queryset = PricingPlan.objects.all()
    serializer_class = PricingPlanSerializer

    def get_permissions(self):

        if self.request.method in ("GET", "HEAD", "OPTIONS"):
            return [AllowAny()]
        return [IsAdminUser()]

    def perform_create(self, serializer):
        name = serializer.validated_data["name"]
        amount = serializer.validated_data["amount"]
        description = serializer.validated_data.get("description", "")
        product = stripe.Product.create(
            name=name,
            description=description,
        )
        price = stripe.Price.create(
            product=product.id,
            unit_amount=amount,
            currency="usd",
            recurring={"interval": "month"},
        )
        serializer.save(stripe_price_id=price.id)




@extend_schema(
    tags=["payment"],
)
class CreateStripeCustomerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        customer_id = get_or_create_stripe_customer(request.user)
        return Response(
            {"stripe_customer_id": customer_id},
            status=status.HTTP_200_OK
        )
    
@extend_schema(tags=["payment"])
class GetStripeCustomerView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        customer_id = get_or_create_stripe_customer(request.user)
        return Response(
            {"stripe_customer_id": customer_id},
            status=status.HTTP_200_OK
        )

@extend_schema(
    tags=["payment"],
)
class AddPaymentMethodView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddPaymentMethodSerializer
    def post(self, request):
        serializer = AddPaymentMethodSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        stripe_profile  = get_or_create_stripe_customer(request.user)
        customer_id = stripe_profile.stripe_customer_id
        pm_id = serializer.validated_data["payment_method_id"]
        try:
    
            stripe.PaymentMethod.attach(pm_id, customer=customer_id)

            stripe.Customer.modify(
                customer_id,
                invoice_settings={"default_payment_method": pm_id}
            )
            stripe_profile.default_payment_method = pm_id
            stripe_profile.has_valid_payment_method = True
            stripe_profile.last_payment_failed = False
            stripe_profile.save(
                update_fields=[
                    "default_payment_method",
                    "has_valid_payment_method",
                    "last_payment_failed",
                ]
            )
        except stripe.error.InvalidRequestError as e:
            return Response(
                {
                    "error": "Invalid payment method",
                    "details": str(e),
                    "action": "Please re-add your card"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        except stripe.error.StripeError:
            return Response(
                {
                    "error": "Payment service temporarily unavailable"
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        return Response(
            {"message": "Payment method added"},
            status=status.HTTP_201_CREATED
        )


@extend_schema(
    tags=["payment"],
)
class ListPaymentMethodsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            customer_id = request.user.stripe_profile.stripe_customer_id
        except StripeCustomer.DoesNotExist:
            return Response([], status=status.HTTP_200_OK)

        pms = stripe.PaymentMethod.list(
            customer=customer_id,
            type="card"
        )

        return Response([
            {
                "id": pm.id,
                "brand": pm.card.brand,
                "last4": pm.card.last4,
                "exp_month": pm.card.exp_month,
                "exp_year": pm.card.exp_year,
            }
            for pm in pms.data
        ])


@extend_schema(
    tags=["payment"],
)
class DeletePaymentMethodView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        stripe.PaymentMethod.detach(id)
        return Response(status=status.HTTP_204_NO_CONTENT)





@extend_schema(
    tags=["payment"],
)
class CreateSetupIntent(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class=SetupIntentResponseSerializer
    def post(self, request):
        user = request.user
        
        subscription, _ = Subscription.objects.get_or_create(user=user)
        full_name = f"{user.first_name} {user.last_name}".strip()
        if not full_name:
            full_name = user.username
        if not subscription.stripe_customer_id:
            customer = stripe.Customer.create(
                email=user.email,
                name=full_name or user.username,
            )
            subscription.stripe_customer_id = customer.id
            subscription.save()
        else:
            customer = stripe.Customer.retrieve(subscription.stripe_customer_id)

        setup_intent = stripe.SetupIntent.create(
            customer=customer.id,
            payment_method_types=["card"],
        )

        return Response({
            "client_secret": setup_intent.client_secret,
            "customer_id": customer.id
        })
    
@extend_schema(
    tags=["payment"],
)
class SubscriptionStatusAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        subscription = getattr(request.user, "subscription", None)

        if not subscription:
            return Response({"is_subscribed": False})

        is_active = (
            subscription.is_active
            and subscription.current_period_end
            and subscription.current_period_end > timezone.now()
        )

        return Response({"is_subscribed": is_active})
