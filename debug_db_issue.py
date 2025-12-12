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

def debug_db_issue():
    print("Debugging database issue...")
    
    # Check user ID 40
    try:
        user_40 = User.objects.get(id=40)
        print(f"User ID 40 exists: {user_40.username} ({user_40.email})")
        
        # Check if this user has a client profile
        try:
            client = user_40.client_profile
            print(f"User 40 has client profile: {client.id}")
        except Client.DoesNotExist:
            print("User 40 does NOT have a client profile")
            
    except User.DoesNotExist:
        print("User ID 40 does NOT exist")
    
    # Check for orphaned client records
    orphaned_clients = Client.objects.filter(user__isnull=True)
    print(f"Orphaned clients (no user): {orphaned_clients.count()}")
    
    # Check for clients with non-existent users
    all_clients = Client.objects.all()
    print(f"Total clients: {all_clients.count()}")
    
    for client in all_clients:
        try:
            user = client.user
            print(f"Client {client.id} -> User {user.id} ({user.username})")
        except User.DoesNotExist:
            print(f"Client {client.id} -> MISSING USER!")
    
    # Check the latest user ID
    latest_user = User.objects.order_by('-id').first()
    if latest_user:
        print(f"Latest user ID: {latest_user.id}")
    
    # Check for any duplicate client records
    from django.db.models import Count
    duplicate_users = Client.objects.values('user_id').annotate(count=Count('user_id')).filter(count__gt=1)
    if duplicate_users:
        print("Found duplicate client records:")
        for dup in duplicate_users:
            print(f"  User ID {dup['user_id']} has {dup['count']} client records")

if __name__ == '__main__':
    debug_db_issue()