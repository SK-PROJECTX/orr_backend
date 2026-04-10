#!/usr/bin/env python
"""
Simple test to verify ContentCard API works with long content.
"""

import requests
import json

def test_content_card_api():
    """Test the ContentCard API with long content"""
    
    # Base URL for the API
    base_url = "https://orr-backend-web-latest.onrender.com/admin-portal/v1/cms"
    
    # Test data with moderately long content
    test_data = {
        "title": {
            "content": "Test Content Card Title " + "X" * 100,
            "format": "html"
        },
        "badge": {
            "content": "Test Badge",
            "format": "html"
        },
        "content": [
            "This is a test content item that should work fine.",
            "Another content item with reasonable length."
        ],
        "image_url": "https://example.com/test-image.jpg",
        "button1_text": {
            "content": "Button 1",
            "format": "html"
        },
        "button2_text": {
            "content": "Button 2",
            "format": "html"
        }
    }
    
    print("Testing ContentCard API with long content...")
    
    # Test updating content card ID 3 (from the error message)
    card_id = 3
    url = f"{base_url}/content-cards/{card_id}/"
    
    try:
        response = requests.put(
            url,
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        print(f"Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✓ ContentCard updated successfully!")
                print(f"  Title length: {len(test_data['title']['content'])} characters")
            else:
                print(f"✗ API returned success=false: {result.get('message')}")
        else:
            print(f"✗ API returned error: {response.status_code}")
            try:
                error_data = response.json()
                print(f"  Error message: {error_data.get('message', 'No message')}")
            except:
                print(f"  Raw response: {response.text[:200]}...")
                
    except requests.exceptions.RequestException as e:
        print(f"✗ Request failed: {e}")
    
    # Test with extremely long content (should be handled gracefully)
    print("\nTesting with extremely long content...")
    
    long_test_data = {
        "title": {
            "content": "Very Long Title " + "A" * 2000,
            "format": "html"
        },
        "badge": {
            "content": "Badge " + "B" * 1000,
            "format": "html"
        }
    }
    
    try:
        response = requests.put(
            url,
            json=long_test_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        print(f"Response Status: {response.status_code}")
        
        if response.status_code in [200, 400]:
            result = response.json()
            if result.get('success'):
                print("✓ Long content handled successfully!")
            else:
                print(f"✓ Long content properly rejected: {result.get('message')}")
        else:
            print(f"? Unexpected response: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"✗ Request failed: {e}")

if __name__ == '__main__':
    test_content_card_api()