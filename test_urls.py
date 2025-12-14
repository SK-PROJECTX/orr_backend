#!/usr/bin/env python
import os
import sys
import django
from django.urls import reverse
from django.test import Client

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.base')
django.setup()

def test_billing_urls():
    """Test if billing URLs are properly configured"""
    try:
        # Test URL reversal
        billing_stats_url = reverse('admin-billing-stats')
        billing_history_url = reverse('admin-billing-history')
        
        print(f"Billing stats URL: {billing_stats_url}")
        print(f"Billing history URL: {billing_history_url}")
        
        # Test with Django test client
        client = Client()
        
        # Test stats endpoint
        response = client.get('/admin-portal/v1/billing-history/stats/')
        print(f"Stats endpoint status: {response.status_code}")
        
        # Test history endpoint  
        response = client.get('/admin-portal/v1/billing-history/')
        print(f"History endpoint status: {response.status_code}")
        
    except Exception as e:
        print(f"URL configuration error: {e}")

if __name__ == "__main__":
    test_billing_urls()