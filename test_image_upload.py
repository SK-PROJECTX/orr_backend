#!/usr/bin/env python3
"""
Test script to verify image upload and business system section update
"""
import requests
import json
import io
from PIL import Image

API_BASE_URL = "http://localhost:8000"

def create_test_image():
    """Create a simple test image"""
    # Create a simple colored image
    img = Image.new('RGB', (300, 200), color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes

def test_login():
    """Test login and get token"""
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
            print("✅ Login successful")
            return data.get('access')
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None

def test_image_upload(token):
    """Test image upload"""
    print("\n🖼️ Testing image upload...")
    
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    # Create test image
    test_image = create_test_image()
    
    files = {
        'image': ('test_business_system.png', test_image, 'image/png')
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

def test_business_system_update(token, image_url):
    """Test business system section update with new image"""
    print("\n🔄 Testing business system section update...")
    
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    update_data = {
        "card_1_image": image_url,
        "card_1_title": "Updated Nervous System"
    }
    
    try:
        response = requests.put(
            f"{API_BASE_URL}/admin-portal/v1/cms/business-system-section/",
            json=update_data,
            headers=headers
        )
        
        print(f"Update Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("✅ Business system section updated!")
            print(f"Updated card_1_image: {data.get('data', {}).get('card_1_image')}")
            return True
        else:
            print(f"❌ Update failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Update error: {e}")
        return False

def test_get_business_system():
    """Test getting business system section"""
    print("\n📖 Testing business system section retrieval...")
    
    try:
        response = requests.get(
            f"{API_BASE_URL}/admin-portal/v1/cms/business-system-section/"
        )
        
        print(f"Get Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("✅ Business system section retrieved!")
            section_data = data.get('data', {})
            print(f"Card 1 Image: {section_data.get('card_1_image')}")
            print(f"Card 1 Title: {section_data.get('card_1_title')}")
            return section_data
        else:
            print(f"❌ Get failed: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Get error: {e}")
        return None

def main():
    print("=== Image Upload & Business System Update Test ===")
    
    # Test login
    token = test_login()
    if not token:
        print("❌ Cannot proceed without authentication")
        return
    
    # Test image upload
    image_url = test_image_upload(token)
    if not image_url:
        print("❌ Cannot proceed without uploaded image")
        return
    
    # Test business system update
    update_success = test_business_system_update(token, image_url)
    if not update_success:
        print("❌ Business system update failed")
        return
    
    # Test retrieval to verify update
    section_data = test_get_business_system()
    if section_data:
        print("\n✅ All tests passed!")
        print("The image upload and business system update workflow is working correctly.")
    else:
        print("\n❌ Final verification failed")

if __name__ == "__main__":
    main()