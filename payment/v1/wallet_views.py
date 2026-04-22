from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import stripe
from django.conf import settings
from common.response import CustomJSONRenderer
from client.models import Wallet, Transaction, Project
from client.v1.serializers.dashboard import WalletSerializer, TransactionSerializer
from payment.models import PricingPlan, Subscription
from django.utils import timezone
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)
stripe.api_key = settings.STRIPE_SECRET_KEY

class WalletBalanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wallet, created = Wallet.objects.get_or_create(owner=request.user)
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)

class TransactionListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wallet, created = Wallet.objects.get_or_create(owner=request.user)
        transactions = wallet.transactions.all().order_by('-date')
        
        # Simple pagination or just return all for now as per current frontend expectation
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

class TopUpView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        amount = request.data.get('amount')
        if not amount:
            return Response({"error": "Amount is required"}, status=400)
        
        try:
            amount_cents = int(float(amount) * 100)
            success_url = request.data.get('success_url', settings.STRIPE_SUCCESS_URL)
            cancel_url = request.data.get('cancel_url', settings.STRIPE_CANCEL_URL)

            # Create a Stripe Checkout Session for Top-up
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Wallet Top-up',
                        },
                        'unit_amount': amount_cents,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=success_url,
                cancel_url=cancel_url,
                metadata={
                    'user_id': request.user.id,
                    'type': 'top_up',
                    'amount': amount
                }
            )
            return Response({"checkout_url": session.url})
        except Exception as e:
            logger.error(f"Top-up error: {str(e)}")
            return Response({"error": str(e)}, status=400)

class PayWithWalletView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        plan_id = request.data.get('plan_id') or request.data.get('invoice_id')
        if not plan_id:
            return Response({"error": "Plan ID or Invoice ID is required"}, status=400)

        try:
            plan = PricingPlan.objects.get(id=plan_id)
            wallet, _ = Wallet.objects.get_or_create(owner=request.user)
            
            plan_amount = Decimal(plan.amount) / Decimal(100)
            
            if wallet.balance < plan_amount:
                return Response({"error": "Insufficient wallet balance"}, status=400)
            
            # Deduct and create transaction
            wallet.balance -= plan_amount
            wallet.save()
            
            Transaction.objects.create(
                wallet=wallet,
                amount=plan_amount,
                transaction_type='withdrawal',
                description=f"Payment for {plan.name} plan"
            )
            
            # Update/Create subscription
            Subscription.objects.update_or_create(
                user=request.user,
                defaults={
                    'plan': plan,
                    'plan_name': plan.name,
                    'is_active': True,
                    'current_period_end': timezone.now() + timezone.timedelta(days=30)
                }
            )
            
            return Response({"message": "Payment successful, subscription activated"}, status=200)
            
        except PricingPlan.DoesNotExist:
            return Response({"error": "Invalid plan"}, status=400)
        except Exception as e:
            logger.error(f"Wallet payment error: {str(e)}")
            return Response({"error": str(e)}, status=400)
