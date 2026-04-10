#!/usr/bin/env python
import os
import sys
import django
import requests

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.base')
django.setup()

from django.contrib.auth.models import User
from admin_portal.models import AdminProfile, AdminRole

def test_login_api():
    """Test the login API endpoint"""
    try:
        # Test with admintest user
        response = requests.post(
            'http://localhost:8000/api/auth/login/',
            json={'username': 'admintest', 'password': 'admintest'},
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            user_data = data['data']['user']
            print(f"\nLogin successful!")
            print(f"User Type: {user_data['user_type']}")
            print(f"Role: {user_data['role']}")
            print(f"Can Edit Content: {user_data['can_edit_content']}")
            print(f"Permissions: {user_data['permissions']}")
        else:
            print(f"\nLogin failed with status {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("Connection failed - Django server is not running")
        print("Start the server with: python manage.py runserver")
    except Exception as e:
        print(f"Error: {e}")

def check_user_setup():
    """Check if the admintest user is properly set up"""
    try:
        user = User.objects.get(username='admintest')
        print(f"User found: {user.username} ({user.email})")
        
        try:
            profile = AdminProfile.objects.get(user=user)
            print(f"Admin profile found: {profile.role.name if profile.role else 'No role'}")
            
            if profile.role:
                print(f"   - Can create content: {profile.role.can_create_content}")
                print(f"   - Can publish content: {profile.role.can_publish_content}")
            
        except AdminProfile.DoesNotExist:
            print("No admin profile found for user")
            
    except User.DoesNotExist:
        print("User 'admintest' not found")

if __name__ == '__main__':
    print("Checking user setup...")
    check_user_setup()
    
    print("\nTesting login API...")
    test_login_api()