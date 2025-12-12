#!/usr/bin/env python
import os
import sys
import django
import json

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.development')
django.setup()

from django.test import Client as TestClient
from django.contrib.auth.models import User
from admin_portal.models import Client, AdminRole, AdminProfile
import uuid

def test_api_endpoint():
    print("Testing client creation API endpoint...")
    
    # Create or get an admin user for authentication
    admin_user, created = User.objects.get_or_create(
        username='test_admin',
        defaults={
            'email': 'test_admin@example.com',
            'is_staff': True,
            'is_superuser': True
        }
    )
    
    if created:
        admin_user.set_password('testpass123')
        admin_user.save()
        print(f"Created admin user: {admin_user.username}")
    else:
        print(f"Using existing admin user: {admin_user.username}")
    
    # Create admin role and profile if needed
    admin_role, _ = AdminRole.objects.get_or_create(
        name='super_admin',
        defaults={
            'description': 'Super Administrator',
            'can_manage_users': True,
            'can_view_all_clients': True,
            'can_edit_clients': True,
            'can_manage_tickets': True,
            'can_manage_meetings': True,
            'can_create_content': True,
            'can_publish_content': True,
            'can_view_analytics': True,
            'can_view_billing': True,
            'can_manage_settings': True,
            'can_view_ai_logs': True,
        }
    )
    
    admin_profile, _ = AdminProfile.objects.get_or_create(
        user=admin_user,
        defaults={
            'role': admin_role,
            'department': 'IT',
            'is_active': True
        }
    )
    
    # Create test client for API calls
    client = TestClient()
    
    # Login the admin user
    login_success = client.login(username='test_admin', password='testpass123')
    if not login_success:
        print("Failed to login admin user")
        return
    
    print("Admin user logged in successfully")
    
    # Generate unique test data
    unique_id = str(uuid.uuid4())[:8]
    test_data = {
        'username': f'apiclient_{unique_id}',
        'email': f'apiclient_{unique_id}@example.com',
        'full_name': f'API Client {unique_id}',
        'company': 'API Test Company',
        'role': 'CTO',
        'stage': 'discover',
        'primary_pillar': 'strategic'
    }
    
    print(f"Test data: {test_data}")
    
    # Make API call to create client
    response = client.post(
        '/admin-portal/v1/clients/',
        data=json.dumps(test_data),
        content_type='application/json'
    )
    
    print(f"API Response Status: {response.status_code}")
    print(f"API Response Content: {response.content.decode()}")
    
    if response.status_code == 201:
        print("[SUCCESS] Client created successfully via API!")
        response_data = json.loads(response.content.decode())
        print(f"Created client ID: {response_data.get('id')}")
        
        # Clean up the created client
        try:
            created_client = Client.objects.get(id=response_data.get('id'))
            created_user = created_client.user
            print(f"Cleaning up client {created_client.id} and user {created_user.username}")
            created_client.delete()
            created_user.delete()
            print("Cleanup completed")
        except Exception as e:
            print(f"Cleanup failed: {e}")
    else:
        print(f"[ERROR] Client creation failed: {response.content.decode()}")

if __name__ == '__main__':
    test_api_endpoint()