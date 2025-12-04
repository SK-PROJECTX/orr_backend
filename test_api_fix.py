#!/usr/bin/env python3
"""
Test script to verify API endpoints and authentication
"""
import requests
import json

API_BASE_URL = "http://localhost:8000"

def test_login():
    """Test login endpoint"""
    print("Testing login endpoint...")
    
    # Test with default Django superuser credentials
    login_data = {
        "username": "admin",  # Change this to your actual username
        "password": "admin"   # Change this to your actual password
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/auth/login/",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Login Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("Login successful!")
            print(f"User: {data.get('user', {}).get('username')}")
            print(f"Role: {data.get('user', {}).get('role')}")
            print(f"Can Edit Content: {data.get('user', {}).get('can_edit_content')}")
            return data.get('access')
        else:
            print(f"Login failed: {response.text}")
            return None
            
    except Exception as e:
        print(f"Login error: {e}")
        return None

def test_cms_endpoints(token=None):
    """Test CMS endpoints"""
    print("\nTesting CMS endpoints...")
    
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    # Test GET business system section (should work without auth)
    try:
        response = requests.get(
            f"{API_BASE_URL}/admin-portal/v1/cms/business-system-section/"
        )
        print(f"GET business-system-section Status: {response.status_code}")
        if response.status_code == 200:
            print("GET request successful!")
        else:
            print(f"GET failed: {response.text}")
    except Exception as e:
        print(f"GET error: {e}")
    
    # Test PUT business system section (requires auth)
    test_data = {
        "title": "Test Update",
        "subtitle": "Test subtitle update"
    }
    
    try:
        response = requests.put(
            f"{API_BASE_URL}/admin-portal/v1/cms/business-system-section/",
            json=test_data,
            headers=headers
        )
        print(f"PUT business-system-section Status: {response.status_code}")
        if response.status_code == 200:
            print("PUT request successful!")
        else:
            print(f"PUT failed: {response.text}")
    except Exception as e:
        print(f"PUT error: {e}")

def test_image_upload(token=None):
    """Test image upload endpoint"""
    print("\nTesting image upload endpoint...")
    
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    # Create a simple test image file
    test_image_content = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\tpHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\nIDATx\x9cc\xf8\x00\x00\x00\x01\x00\x01\x00\x00\x00\x00IEND\xaeB`\x82'
    
    files = {
        'image': ('test.png', test_image_content, 'image/png')
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/admin-portal/v1/cms/upload-image/",
            files=files,
            headers=headers
        )
        print(f"Image upload Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("Image upload successful!")
            print(f"Image URL: {data.get('image_url')}")
        else:
            print(f"Image upload failed: {response.text}")
    except Exception as e:
        print(f"Image upload error: {e}")

def main():
    print("=== API Test Script ===")
    
    # Test login
    token = test_login()
    
    # Test CMS endpoints
    test_cms_endpoints(token)
    
    # Test image upload
    test_image_upload(token)
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    main()