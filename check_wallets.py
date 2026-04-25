import os
import django
import sys

# Set up Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orr.settings')
django.setup()

from client.models import Wallet
from django.contrib.auth.models import User

print("--- Wallet Balances ---")
wallets = Wallet.objects.select_related('owner').all()
for w in wallets:
    print(f"User: {w.owner.email} | Balance: {w.balance} | Name: {w.owner.get_full_name()} | Username: {w.owner.username}")

print("\n--- Paid Invoices ---")
from payment.models import Invoice
paid_invoices = Invoice.objects.filter(status__icontains='paid')
for inv in paid_invoices:
    print(f"Invoice: {inv.stripe_invoice_id} | User: {inv.user.email} | Amount: {inv.amount} | Status: {inv.status}")
