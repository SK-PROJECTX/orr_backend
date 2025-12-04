from django.utils import timezone
from admin_portal.models import Ticket, Client
from payment.models import Invoice, Subscription


class PaymentTicketService:
    """Service for creating payment-related tickets automatically"""
    
    @staticmethod
    def create_payment_failed_ticket(invoice):
        """Create ticket for failed payment"""
        try:
            client = Client.objects.get(user=invoice.user)
            
            ticket = Ticket.objects.create(
                client=client,
                subject=f"Payment Failed - Invoice {invoice.stripe_invoice_id}",
                description=f"Payment failed for invoice {invoice.stripe_invoice_id}. Amount: ${invoice.amount}",
                status="payment_failed",
                priority="high",
                source="payment_webhook",
                related_invoice=invoice,
                payment_amount=invoice.amount,
            )
            
            return ticket
        except Client.DoesNotExist:
            return None
    
    @staticmethod
    def create_subscription_cancelled_ticket(subscription):
        """Create ticket for cancelled subscription"""
        try:
            client = Client.objects.get(user=subscription.user)
            
            ticket = Ticket.objects.create(
                client=client,
                subject=f"Subscription Cancelled - {subscription.plan_name}",
                description=f"Subscription {subscription.stripe_subscription_id} has been cancelled.",
                status="processing",
                priority="normal",
                source="payment_webhook",
                related_subscription=subscription,
                payment_amount=0,
            )
            
            return ticket
        except Client.DoesNotExist:
            return None
    
    @staticmethod
    def create_dispute_ticket(invoice):
        """Create ticket for payment dispute"""
        try:
            client = Client.objects.get(user=invoice.user)
            
            ticket = Ticket.objects.create(
                client=client,
                subject=f"Payment Disputed - Invoice {invoice.stripe_invoice_id}",
                description=f"Payment dispute raised for invoice {invoice.stripe_invoice_id}. Amount: ${invoice.amount}",
                status="payment_disputed",
                priority="urgent",
                source="payment_webhook",
                related_invoice=invoice,
                payment_amount=invoice.amount,
            )
            
            return ticket
        except Client.DoesNotExist:
            return None
    
    @staticmethod
    def create_refund_request_ticket(invoice, refund_amount):
        """Create ticket for refund request"""
        try:
            client = Client.objects.get(user=invoice.user)
            
            ticket = Ticket.objects.create(
                client=client,
                subject=f"Refund Requested - Invoice {invoice.stripe_invoice_id}",
                description=f"Refund requested for invoice {invoice.stripe_invoice_id}. Refund amount: ${refund_amount}",
                status="refund_requested",
                priority="normal",
                source="billing_portal",
                related_invoice=invoice,
                payment_amount=invoice.amount,
                refund_amount=refund_amount,
            )
            
            return ticket
        except Client.DoesNotExist:
            return None