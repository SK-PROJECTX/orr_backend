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

def check_db_state():
    print("Checking database state...")
    
    # Check for orphaned users (users without client profiles)
    users_without_clients = User.objects.filter(client_profile__isnull=True)
    print(f"Users without client profiles: {users_without_clients.count()}")
    
    for user in users_without_clients[:10]:  # Show first 10
        print(f"  - {user.username} ({user.email}) - ID: {user.id}")
    
    # Check for clients
    clients = Client.objects.all()
    print(f"Total clients: {clients.count()}")
    
    # Check for users with client profiles
    users_with_clients = User.objects.filter(client_profile__isnull=False)
    print(f"Users with client profiles: {users_with_clients.count()}")
    
    # Check for specific test user
    test_users = User.objects.filter(username__startswith='testuser')
    print(f"Test users found: {test_users.count()}")
    for user in test_users:
        print(f"  - {user.username} - ID: {user.id}")
        try:
            client = user.client_profile
            print(f"    Has client profile: {client.id}")
        except Client.DoesNotExist:
            print(f"    No client profile")

if __name__ == '__main__':
    check_db_state()