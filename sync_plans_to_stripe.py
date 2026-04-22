import os
import sys
import django
import stripe

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.development')
django.setup()

from payment.models import PricingPlan
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def sync_plans():
    print(f"Starting Stripe Plan Sync (Environment: {os.environ.get('DJANGO_SETTINGS_MODULE')})")
    print(f"Using Stripe Key: {stripe.api_key[:10]}...{stripe.api_key[-4:]}")
    
    plans = PricingPlan.objects.all()
    
    if not plans:
        print("No Pricing Plans found in the database. Check your database connection.")
        return

    for plan in plans:
        print(f"\n--- Syncing Plan: {plan.name} ---")
        print(f"Current ID: {plan.stripe_price_id}")
        
        try:
            # Create a real Product in Stripe
            product = stripe.Product.create(
                name=plan.name,
                description=plan.description or f"Plan: {plan.name}",
            )
            print(f"Created Stripe Product: {product.id}")
            
            # Create a real Price in Stripe
            price_params = {
                "product": product.id,
                "unit_amount": int(plan.amount),
                "currency": "usd",
            }
            
            if plan.billing_type == 'monthly':
                price_params["recurring"] = {"interval": "month"}
            elif plan.billing_type == 'metered':
                # Metered billing for hourly plans
                price_params["recurring"] = {
                    "interval": "month",
                    "usage_type": "metered",
                }
            
            price = stripe.Price.create(**price_params)
            print(f"Created Stripe Price: {price.id} (Type: {plan.billing_type})")
            
            # Update database
            old_id = plan.stripe_price_id
            plan.stripe_price_id = price.id
            plan.save()
            print(f"Updated DB: {old_id} -> {plan.stripe_price_id}")
            
        except Exception as e:
            print(f"Error syncing {plan.name}: {str(e)}")

    print("\nSync completed for all plans.")

if __name__ == "__main__":
    sync_plans()
