import datetime
from rest_framework import viewsets, status
import stripe
from django.conf import settings
from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from ..models import Invoice, Subscription, PricingPlan
from .serializers import (
    BillingPortalSerializer,
    ChangePlanSerializer,
    CreateCheckoutSerializer,
    InvoiceHistorySerializer,
    PauseSubscriptionSerializer,
    PricingPlanSerializer,
)
from common.permissions import IsAdminUser
stripe.api_key = settings.STRIPE_SECRET_KEY

User = settings.AUTH_USER_MODEL

@extend_schema(
    tags=["payment"],)
class CreateCheckoutSession(APIView):
    serializer_class = CreateCheckoutSerializer
    permission_classes = [IsAuthenticated]
    def post(self, request):
        price_id = request.data.get("price_id")

        if not price_id:
            return Response({"error": "price_id is required"}, status=400)

        try:
            session = stripe.checkout.Session.create(
                mode="subscription",
                payment_method_types=["card"],
                line_items=[{"price": price_id, "quantity": 1}],
                success_url=settings.STRIPE_SUCCESS_URL + "?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=settings.STRIPE_CANCEL_URL,
            )

            return Response({"checkout_url": session.url})

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except Exception:
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        data = event["data"]["object"]

        customer_id = data["customer"]
        subscription_id = data["subscription"]
        email = data.get("customer_details", {}).get("email")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return HttpResponse(status=200)

        stripe_sub = stripe.Subscription.retrieve(subscription_id)

        plan_name = stripe_sub["items"]["data"][0]["plan"]["nickname"]
        current_period_end = timezone.datetime.fromtimestamp(
            stripe_sub["current_period_end"], timezone.utc
        )
        Subscription.objects.update_or_create(
            user=user,
            defaults={
                "stripe_subscription_id": subscription_id,
                "stripe_customer_id": customer_id,
                "plan_name": plan_name,
                "is_active": True,
                "current_period_end": current_period_end,
            },
        )
        if event["type"] == "customer.subscription.deleted":
            data = event["data"]["object"]
            subscription_id = data["id"]

            try:
                sub = Subscription.objects.get(stripe_subscription_id=subscription_id)
                sub.is_active = False
                sub.save()

                sub.user.is_active = False
                sub.user.save()

            except Subscription.DoesNotExist:
                pass

    return HttpResponse(status=200)

@extend_schema(
    tags=["payment"],)
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
    tags=["payment"],)
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
    tags=["payment"],)
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
    tags=["payment"],)
class StripeWebhookView(APIView):

    def post(self, request):
        payload = request.body
        sig = request.META.get("HTTP_STRIPE_SIGNATURE")

        try:
            event = stripe.Webhook.construct_event(
                payload, sig, settings.STRIPE_WEBHOOK_SECRET
            )
        except Exception:
            return HttpResponse(status=400)
        if event["type"] == "invoice.payment_succeeded":
            data = event["data"]["object"]

            user = User.objects.filter(customer_id=data["customer"]).first()
            if not user:
                return HttpResponse(status=200)

            invoice_number = data.get("number") or data["id"]
            billing_date = datetime.fromtimestamp(data["created"]).date()

            Invoice.objects.update_or_create(
                stripe_invoice_id=data["id"],
                defaults={
                    "user": user,
                    "billing_title": f"Billing #{invoice_number} – {billing_date.strftime('%b %Y')}",
                    "status": data["status"].capitalize(),
                    "billing_date": billing_date,
                    "amount": data["amount_paid"] / 100,
                    "currency": data["currency"].upper(),
                    "plan": (
                        data["lines"]["data"][0]["plan"]["nickname"]
                        if data["lines"]["data"]
                        else "Unknown"
                    ),
                    "users": (
                        data["lines"]["data"][0]["quantity"]
                        if data["lines"]["data"]
                        else 1
                    ),
                    "invoice_pdf": data.get("invoice_pdf"),
                    "hosted_invoice_url": data.get("hosted_invoice_url"),
                },
            )

        return HttpResponse(status=200)
    
@extend_schema(
    tags=["payment"],)
class BillingHistoryView(ListAPIView):
    serializer_class = InvoiceHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Invoice.objects.filter(user=self.request.user).order_by("-created_at")


@extend_schema(
    tags=["payment"],)
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