#!/usr/bin/env python
import os
import sys
import django
import requests

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.development')
django.setup()

def test_billing_endpoint():
    """Test the billing stats endpoint"""
    try:
        # Test the endpoint directly
        url = "http://127.0.0.1:8000/admin-portal/v1/billing-history/stats/"
        print(f"Testing URL: {url}")
        
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Endpoint is working!")
        else:
            print("❌ Endpoint failed!")
            
    except Exception as e:
        print(f"❌ Error testing endpoint: {e}")

if __name__ == "__main__":
    test_billing_endpoint()