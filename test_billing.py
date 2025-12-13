#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.base')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

# Create a test client
client = Client()

# Test the billing endpoints
print("Testing billing endpoints...")

try:
    # Test billing history endpoint
    response = client.get('/admin-portal/v1/billing-history/')
    print(f"Billing History Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.json()}")
    else:
        print(f"Error: {response.content}")
    
    # Test billing stats endpoint
    response = client.get('/admin-portal/v1/billing-history/stats/')
    print(f"Billing Stats Status: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.json()}")
    else:
        print(f"Error: {response.content}")
        
except Exception as e:
    print(f"Error: {e}")