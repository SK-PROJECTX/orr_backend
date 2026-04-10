#!/usr/bin/env python
"""
Test Login Endpoint
Test the login endpoint to ensure it's working correctly
"""

import requests
import json

def test_login_endpoint():
    """Test the login endpoint with various scenarios"""
    
    base_url = "http://127.0.0.1:8002"
    login_url = f"{base_url}/login/"
    
    print("Testing login endpoint...")
    print(f"URL: {login_url}")
    print("=" * 50)
    
    # Test 1: Missing credentials
    print("Test 1: Missing credentials")
    try:
        response = requests.post(login_url, json={})
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {str(e)}")
    print()
    
    # Test 2: Invalid credentials
    print("Test 2: Invalid credentials")
    try:
        response = requests.post(login_url, json={
            "username": "invalid_user",
            "password": "invalid_pass"
        })
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {str(e)}")
    print()
    
    # Test 3: Valid admin credentials (if exists)
    print("Test 3: Valid admin credentials")
    try:
        response = requests.post(login_url, json={
            "username": "admin",
            "password": "admin123"
        })
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("Login successful!")
            print(f"User type: {data.get('data', {}).get('user', {}).get('user_type')}")
            print(f"Access token length: {len(data.get('data', {}).get('accessToken', ''))}")
        else:
            print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {str(e)}")
    print()
    
    # Test 4: Check if server is running
    print("Test 4: Server health check")
    try:
        response = requests.get(f"{base_url}/api/schema/")
        print(f"Schema endpoint status: {response.status_code}")
    except Exception as e:
        print(f"Server connection error: {str(e)}")
        print("Make sure the Django server is running on port 8002")

if __name__ == "__main__":
    test_login_endpoint()