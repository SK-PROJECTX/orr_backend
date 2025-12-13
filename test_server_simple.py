#!/usr/bin/env python
"""
Simple Server Test
Test if the Django server is running and responding
"""

import requests
import json

def test_server():
    """Test basic server functionality"""
    
    base_url = "http://127.0.0.1:8002"
    
    print("Testing Django server...")
    print(f"Base URL: {base_url}")
    print("=" * 40)
    
    # Test 1: Check if server is running
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        print(f"Root endpoint status: {response.status_code}")
    except Exception as e:
        print(f"Server connection failed: {str(e)}")
        return False
    
    # Test 2: Check login endpoint exists
    try:
        response = requests.post(f"{base_url}/login/", json={}, timeout=5)
        print(f"Login endpoint status: {response.status_code}")
        if response.status_code == 400:
            print("Login endpoint exists (400 = missing credentials)")
        elif response.status_code == 404:
            print("Login endpoint NOT FOUND")
            return False
    except Exception as e:
        print(f"Login endpoint test failed: {str(e)}")
        return False
    
    # Test 3: Test with valid format
    try:
        response = requests.post(f"{base_url}/login/", json={
            "username": "test",
            "password": "test"
        }, timeout=5)
        print(f"Login with credentials status: {response.status_code}")
        if response.status_code in [400, 401]:
            print("Login endpoint working (expecting 400/401 for invalid creds)")
            try:
                data = response.json()
                print(f"Response: {data}")
            except:
                pass
    except Exception as e:
        print(f"Login test failed: {str(e)}")
    
    return True

if __name__ == "__main__":
    if test_server():
        print("\nServer appears to be working!")
    else:
        print("\nServer has issues!")