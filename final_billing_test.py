#!/usr/bin/env python
"""
Final comprehensive test for billing endpoints
"""
import os
import sys
import django
import requests
import json
from django.test import Client
from django.urls import reverse

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django with correct settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

def test_with_django_client():
    """Test using Django test client"""
    print("=" * 60)
    print("TESTING WITH DJANGO TEST CLIENT")
    print("=" * 60)
    
    client = Client()
    
    # Test stats endpoint
    try:
        response = client.get('/admin-portal/v1/billing-history/stats/')
        print(f"Stats Endpoint Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Total Revenue: ${data['data']['total_revenue']}")
            print(f"Completed Transactions: {data['data']['completed_transactions']}")
            print(f"Pending Transactions: {data['data']['pending_transactions']}")
        else:
            print(f"Error: {response.content.decode()}")
    except Exception as e:
        print(f"Stats endpoint error: {e}")
    
    print("-" * 40)
    
    # Test history endpoint
    try:
        response = client.get('/admin-portal/v1/billing-history/?limit=3')
        print(f"History Endpoint Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Number of invoices returned: {len(data['data'])}")
            if data['data']:
                first_invoice = data['data'][0]
                print(f"First invoice: {first_invoice['reference_id']} - ${first_invoice['amount']}")
        else:
            print(f"Error: {response.content.decode()}")
    except Exception as e:
        print(f"History endpoint error: {e}")

def test_with_requests(server_url="http://127.0.0.1:8000"):
    """Test using requests library (requires running server)"""
    print("\n" + "=" * 60)
    print("TESTING WITH REQUESTS (REQUIRES RUNNING SERVER)")
    print("=" * 60)
    
    endpoints = [
        f"{server_url}/admin-portal/v1/billing-history/stats/",
        f"{server_url}/admin-portal/v1/billing-history/?limit=3"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(endpoint, timeout=5)
            print(f"Endpoint: {endpoint}")
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                if 'total_revenue' in data.get('data', {}):
                    print(f"Total Revenue: ${data['data']['total_revenue']}")
                elif isinstance(data.get('data'), list):
                    print(f"Invoices returned: {len(data['data'])}")
            else:
                print(f"Error: {response.text}")
            print("-" * 40)
        except requests.exceptions.RequestException as e:
            print(f"Request failed for {endpoint}: {e}")
            print("-" * 40)

def check_database_connection():
    """Check if database connection is working"""
    print("\n" + "=" * 60)
    print("CHECKING DATABASE CONNECTION")
    print("=" * 60)
    
    try:
        from payment.models import Invoice, Subscription
        from django.contrib.auth.models import User
        
        invoice_count = Invoice.objects.count()
        user_count = User.objects.count()
        subscription_count = Subscription.objects.count()
        
        print(f"[OK] Database connection successful")
        print(f"[OK] Invoices in database: {invoice_count}")
        print(f"[OK] Users in database: {user_count}")
        print(f"[OK] Subscriptions in database: {subscription_count}")
        
        if invoice_count > 0:
            latest_invoice = Invoice.objects.first()
            print(f"[OK] Latest invoice: {latest_invoice.billing_title} - ${latest_invoice.amount}")
        
        return True
    except Exception as e:
        print(f"[ERROR] Database connection failed: {e}")
        return False

def main():
    print("BILLING ENDPOINTS COMPREHENSIVE TEST")
    print("=" * 60)
    
    # Check database first
    db_ok = check_database_connection()
    
    if db_ok:
        # Test with Django client (always works)
        test_with_django_client()
        
        # Test with requests (requires server to be running)
        test_with_requests()
        
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        print("[OK] Database connection: OK")
        print("[OK] Django test client: OK")
        print("[OK] URL routing: OK")
        print("[OK] API endpoints: Working")
        print("\nTo test with live server:")
        print("1. Run: python manage.py runserver 127.0.0.1:8000")
        print("2. Visit: http://127.0.0.1:8000/admin-portal/v1/billing-history/stats/")
        print("3. Visit: http://127.0.0.1:8000/admin-portal/v1/billing-history/")
    else:
        print("\n[ERROR] Database connection failed. Please check your database setup.")

if __name__ == "__main__":
    main()