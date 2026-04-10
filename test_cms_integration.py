#!/usr/bin/env python3
"""
Test script to verify CMS integration works properly
"""

import requests
import json

# Configuration
API_BASE_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"

def test_cms_endpoints():
    """Test all CMS endpoints"""
    print("Testing CMS API endpoints...")
    
    endpoints = [
        "/admin-portal/v1/cms/all-content/",
        "/admin-portal/v1/cms/homepage/",
        "/admin-portal/v1/cms/approach-section/",
        "/admin-portal/v1/cms/business-system-section/",
        "/admin-portal/v1/cms/orr-role-section/",
        "/admin-portal/v1/cms/message-strip/",
        "/admin-portal/v1/cms/process-section/",
        "/admin-portal/v1/cms/orr-report-section/",
        "/admin-portal/v1/cms/service-cards/",
        "/admin-portal/v1/cms/faqs/",
        "/admin-portal/v1/cms/testimonials/",
        "/admin-portal/v1/cms/contact-info/",
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{API_BASE_URL}{endpoint}")
            if response.status_code == 200:
                print(f"✅ {endpoint} - OK")
            else:
                print(f"❌ {endpoint} - Status: {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint} - Error: {str(e)}")

def test_content_update():
    """Test content update functionality"""
    print("\nTesting content updates...")
    
    # Test homepage update
    try:
        # First get current content
        response = requests.get(f"{API_BASE_URL}/admin-portal/v1/cms/homepage/")
        if response.status_code == 200:
            print("✅ Homepage GET - OK")
            
            # Try to update (this will require authentication in real scenario)
            update_data = {
                "hero_title": "Test Update - ORR Solutions"
            }
            # Note: This will fail without authentication, but we can test the endpoint exists
            update_response = requests.put(
                f"{API_BASE_URL}/admin-portal/v1/cms/homepage/",
                json=update_data
            )
            if update_response.status_code in [200, 401, 403]:  # 401/403 expected without auth
                print("✅ Homepage PUT endpoint exists")
            else:
                print(f"❌ Homepage PUT - Unexpected status: {update_response.status_code}")
        else:
            print(f"❌ Homepage GET - Status: {response.status_code}")
    except Exception as e:
        print(f"❌ Homepage test - Error: {str(e)}")

def test_comprehensive_endpoint():
    """Test the new comprehensive all-content endpoint"""
    print("\nTesting comprehensive content endpoint...")
    
    try:
        response = requests.get(f"{API_BASE_URL}/admin-portal/v1/cms/all-content/")
        if response.status_code == 200:
            data = response.json()
            
            # Check if all expected sections are present
            expected_sections = [
                'homepage', 'approach_section', 'business_system_section',
                'orr_role_section', 'message_strip', 'process_section',
                'orr_report_section', 'contact_info', 'service_cards',
                'faqs', 'testimonials'
            ]
            
            content_data = data.get('data', data)
            missing_sections = []
            
            for section in expected_sections:
                if section not in content_data:
                    missing_sections.append(section)
            
            if not missing_sections:
                print("✅ All content sections present in comprehensive endpoint")
                print(f"   - Homepage title: {content_data.get('homepage', {}).get('hero_title', 'N/A')}")
                print(f"   - Service cards count: {len(content_data.get('service_cards', []))}")
                print(f"   - FAQs count: {len(content_data.get('faqs', []))}")
            else:
                print(f"❌ Missing sections: {missing_sections}")
        else:
            print(f"❌ Comprehensive endpoint - Status: {response.status_code}")
    except Exception as e:
        print(f"❌ Comprehensive endpoint test - Error: {str(e)}")

def main():
    print("🚀 Starting CMS Integration Tests")
    print("=" * 50)
    
    test_cms_endpoints()
    test_content_update()
    test_comprehensive_endpoint()
    
    print("\n" + "=" * 50)
    print("✨ CMS Integration Tests Complete!")
    print("\n📝 Next Steps:")
    print("1. Start the Django backend: python manage.py runserver")
    print("2. Start the Next.js frontend: npm run dev")
    print("3. Visit http://localhost:3000 to see the homepage")
    print("4. Login as admin to edit content inline")

if __name__ == "__main__":
    main()