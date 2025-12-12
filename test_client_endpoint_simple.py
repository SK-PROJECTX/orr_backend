#!/usr/bin/env python
import os
import sys
import django
import requests
import json

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.development')
django.setup()

def test_client_endpoint_simple():
    print("Testing client creation endpoint with requests...")
    
    # First, let's try to login and get a JWT token
    login_url = "http://127.0.0.1:8000/api/auth/login/"
    login_data = {
        "username": "testadmin",
        "password": "testpass123"
    }
    
    print("Attempting to login...")
    try:
        login_response = requests.post(login_url, json=login_data)
        print(f"Login response status: {login_response.status_code}")
        print(f"Login response: {login_response.text}")
        
        if login_response.status_code == 200:
            login_result = login_response.json()
            # The token is in data.accessToken
            data = login_result.get('data', {})
            access_token = data.get('accessToken')
            
            if access_token:
                print("Login successful, got access token")
                
                # Now test client creation
                client_url = "http://127.0.0.1:8000/admin-portal/v1/clients/"
                headers = {
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json"
                }
                
                client_data = {
                    "username": "testclient_simple",
                    "email": "testclient_simple@example.com",
                    "full_name": "Test Client Simple",
                    "company": "Simple Test Co",
                    "role": "Manager",
                    "stage": "discover",
                    "primary_pillar": "strategic"
                }
                
                print("Creating client...")
                client_response = requests.post(client_url, json=client_data, headers=headers)
                print(f"Client creation response status: {client_response.status_code}")
                print(f"Client creation response: {client_response.text}")
                
                if client_response.status_code == 201:
                    print("[SUCCESS] Client created successfully!")
                else:
                    print(f"[ERROR] Client creation failed with status {client_response.status_code}")
            else:
                print("No access token in login response")
        else:
            print(f"Login failed with status {login_response.status_code}")
            
    except Exception as e:
        print(f"Error during test: {e}")

if __name__ == '__main__':
    test_client_endpoint_simple()