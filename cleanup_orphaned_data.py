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

def cleanup_orphaned_data():
    print("Cleaning up orphaned data...")
    
    # Find and delete test users and their client profiles
    test_users = User.objects.filter(username__startswith='newclient_')
    print(f"Found {test_users.count()} test users to clean up")
    
    for user in test_users:
        print(f"Cleaning up user: {user.username} (ID: {user.id})")
        try:
            if hasattr(user, 'client_profile'):
                client = user.client_profile
                print(f"  - Deleting client profile: {client.id}")
                client.delete()
        except:
            pass
        user.delete()
        print(f"  - Deleted user: {user.username}")
    
    print("Cleanup completed!")

if __name__ == '__main__':
    cleanup_orphaned_data()