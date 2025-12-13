#!/usr/bin/env python
import os
import sys
import django
from django.urls import resolve, reverse
from django.conf import settings

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

def verify_billing_urls():
    """Verify billing URL patterns exist"""
    
    # Test URL patterns
    test_urls = [
        '/admin-portal/v1/billing-history/stats/',
        '/admin-portal/v1/billing-history/',
    ]
    
    for url in test_urls:
        try:
            match = resolve(url)
            print(f"URL exists: {url}")
            print(f"  View: {match.func.__name__}")
            print(f"  View class: {match.func.view_class.__name__}")
            print()
        except Exception as e:
            print(f"URL not found: {url}")
            print(f"  Error: {e}")
            print()
    
    # Test reverse URL lookup
    try:
        stats_url = reverse('admin-billing-stats')
        history_url = reverse('admin-billing-history')
        print(f"Reverse lookup works:")
        print(f"  admin-billing-stats -> {stats_url}")
        print(f"  admin-billing-history -> {history_url}")
    except Exception as e:
        print(f"Reverse lookup failed: {e}")

if __name__ == "__main__":
    verify_billing_urls()