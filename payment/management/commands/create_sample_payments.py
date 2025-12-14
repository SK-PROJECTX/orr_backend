from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
import random

from payment.models import Invoice, Subscription, PricingPlan


class Command(BaseCommand):
    help = 'Create sample payment data for testing'

    def handle(self, *args, **options):
        # Create sample users if they don't exist
        users = []
        for i in range(5):
            user, created = User.objects.get_or_create(
                username=f'testuser{i}',
                defaults={
                    'email': f'testuser{i}@example.com',
                    'first_name': f'Test{i}',
                    'last_name': 'User'
                }
            )
            users.append(user)
            if created:
                self.stdout.write(f'Created user: {user.username}')

        # Create sample pricing plans
        plans = []
        plan_data = [
            {'name': 'Basic Plan', 'amount': 2999},  # $29.99
            {'name': 'Pro Plan', 'amount': 4999},   # $49.99
            {'name': 'Enterprise Plan', 'amount': 9999}  # $99.99
        ]
        
        for plan_info in plan_data:
            plan, created = PricingPlan.objects.get_or_create(
                name=plan_info['name'],
                defaults={
                    'stripe_price_id': f"price_{plan_info['name'].lower().replace(' ', '_')}",
                    'amount': plan_info['amount'],
                    'description': f"Sample {plan_info['name']}"
                }
            )
            plans.append(plan)
            if created:
                self.stdout.write(f'Created plan: {plan.name}')

        # Create sample subscriptions
        for user in users:
            subscription, created = Subscription.objects.get_or_create(
                user=user,
                defaults={
                    'stripe_subscription_id': f'sub_{user.username}',
                    'stripe_customer_id': f'cus_{user.username}',
                    'plan_name': random.choice(plans).name,
                    'is_active': random.choice([True, False]),
                    'current_period_end': timezone.now() + timedelta(days=30)
                }
            )
            if created:
                self.stdout.write(f'Created subscription for: {user.username}')

        # Create sample invoices
        statuses = ['Paid', 'Pending', 'Failed', 'Refunded']
        
        for i in range(20):
            user = random.choice(users)
            plan = random.choice(plans)
            status = random.choice(statuses)
            
            # Random date within last 6 months
            days_ago = random.randint(1, 180)
            billing_date = (timezone.now() - timedelta(days=days_ago)).date()
            
            invoice, created = Invoice.objects.get_or_create(
                stripe_invoice_id=f'inv_{user.username}_{i}',
                defaults={
                    'user': user,
                    'billing_title': f'Invoice #{1000 + i} - {billing_date.strftime("%b %Y")}',
                    'status': status,
                    'billing_date': billing_date,
                    'amount': plan.amount / 100,  # Convert cents to dollars
                    'currency': 'USD',
                    'plan': plan.name,
                    'users': 1,
                    'invoice_pdf': f'https://example.com/invoice_{i}.pdf',
                    'hosted_invoice_url': f'https://example.com/hosted_invoice_{i}'
                }
            )
            
            if created:
                self.stdout.write(f'Created invoice: {invoice.billing_title}')

        self.stdout.write(
            self.style.SUCCESS('Successfully created sample payment data!')
        )