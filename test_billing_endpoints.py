#!/usr/bin/env python
import os
import sys
import django
import requests
from django.test import Client
from django.urls import reverse

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.development')
django.setup()

def test_billing_endpoints():
    """Test billing endpoints using Django test client"""
    client = Client()
    
    # Test endpoints
    endpoints = [
        '/admin-portal/v1/billing-history/stats/',
        '/admin-portal/v1/billing-history/',
        '/admin-portal/v1/billing-history/?limit=5'
    ]
    
    for endpoint in endpoints:
        try:
            response = client.get(endpoint)
            print(f"Endpoint: {endpoint}")
            print(f"Status Code: {response.status_code}")
            if response.status_code == 200:
                print(f"Response: {response.json()}")
            else:
                print(f"Error: {response.content.decode()}")
            print("-" * 50)
        except Exception as e:
            print(f"Exception for {endpoint}: {e}")
            print("-" * 50)

def test_url_reverse():
    """Test URL reverse lookup"""
    try:
        stats_url = reverse('admin-billing-stats')
        history_url = reverse('admin-billing-history')
        print(f"URL Reverse Test:")
        print(f"admin-billing-stats -> {stats_url}")
        print(f"admin-billing-history -> {history_url}")
    except Exception as e:
        print(f"URL Reverse Error: {e}")

if __name__ == "__main__":
    print("Testing Billing Endpoints...")
    test_url_reverse()
    print("\n" + "="*50 + "\n")
    test_billing_endpoints()