#!/usr/bin/env python3
"""
Test authentication flow for image upload
"""
import requests
import json

API_BASE_URL = "http://localhost:8000"

def test_auth_flow():
    print("=== Testing Authentication Flow ===")
    
    # Step 1: Login
    print("\n1. Testing login...")
    login_data = {
        "username": "editor",
        "password": "editor123"
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/auth/login/",
            json=login_data
        )
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('access')
            print(f"✅ Login successful, token: {token[:20]}...")
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(response.text)
            return
    except Exception as e:
        print(f"❌ Login error: {e}")
        return
    
    # Step 2: Test authenticated image upload
    print("\n2. Testing authenticated image upload...")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # Create a simple test file
    test_image_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde'
    
    files = {
        'image': ('test.png', test_image_data, 'image/png')
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/admin-portal/v1/cms/upload-image/",
            files=files,
            headers=headers
        )
        
        print(f"Upload Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("✅ Image upload successful!")
            print(f"Image URL: {data.get('image_url')}")
            return data.get('image_url')
        else:
            print(f"❌ Image upload failed: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Image upload error: {e}")
        return None
    
    # Step 3: Test unauthenticated upload (should fail)
    print("\n3. Testing unauthenticated image upload (should fail)...")
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/admin-portal/v1/cms/upload-image/",
            files=files
        )
        
        print(f"Unauthenticated Upload Status: {response.status_code}")
        if response.status_code == 401:
            print("✅ Correctly rejected unauthenticated upload")
        else:
            print(f"❌ Should have been 401, got: {response.status_code}")
    except Exception as e:
        print(f"❌ Unauthenticated upload test error: {e}")

if __name__ == "__main__":
    test_auth_flow()