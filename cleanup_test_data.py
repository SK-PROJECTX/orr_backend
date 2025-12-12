#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.development')
django.setup()

from django.contrib.auth.models import User
from admin_portal.models import Client

def cleanup_test_data():
    print("Cleaning up test data...")
    
    # Delete test users and their client profiles
    test_users = User.objects.filter(username__startswith='testuser')
    print(f"Found {test_users.count()} test users to delete")
    
    for user in test_users:
        print(f"Deleting user: {user.username}")
        try:
            if hasattr(user, 'client_profile'):
                print(f"  - Also deleting client profile: {user.client_profile.id}")
        except:
            pass
        user.delete()
    
    print("Cleanup completed!")

if __name__ == '__main__':
    cleanup_test_data()