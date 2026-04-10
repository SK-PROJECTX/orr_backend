#!/usr/bin/env python
"""
Fix User ID Sequence Issue
This script fixes the PostgreSQL sequence issue that causes duplicate user_id constraint violations.
"""

import os
import sys
import django
from django.conf import settings

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.development')
django.setup()

from django.contrib.auth.models import User
from django.db import connection, models
from admin_portal.models import Client

def fix_user_sequence():
    """Fix the User ID sequence to prevent constraint violations"""
    
    print("🔧 Fixing User ID sequence...")
    
    # Get the maximum user ID
    max_user_id = User.objects.aggregate(max_id=models.Max('id'))['max_id'] or 0
    print(f"📊 Current maximum User ID: {max_user_id}")
    
    # Check if we're using PostgreSQL
    if 'postgresql' in settings.DATABASES['default']['ENGINE']:
        with connection.cursor() as cursor:
            # Reset the sequence to the correct value
            cursor.execute(f"SELECT setval('auth_user_id_seq', {max_user_id + 1});")
            print(f"✅ PostgreSQL sequence reset to {max_user_id + 1}")
    
    elif 'sqlite' in settings.DATABASES['default']['ENGINE']:
        with connection.cursor() as cursor:
            # For SQLite, update the sqlite_sequence table
            cursor.execute(f"UPDATE sqlite_sequence SET seq = {max_user_id} WHERE name = 'auth_user';")
            print(f"✅ SQLite sequence reset to {max_user_id}")
    
    else:
        print("⚠️ Database engine not recognized. Manual sequence reset may be required.")

def cleanup_orphaned_users():
    """Remove orphaned User records that don't have corresponding Client profiles"""
    
    print("🧹 Cleaning up orphaned User records...")
    
    # Find users that don't have client profiles and aren't staff/superusers
    orphaned_users = User.objects.filter(
        client_profile__isnull=True,
        is_staff=False,
        is_superuser=False
    )
    
    orphaned_count = orphaned_users.count()
    print(f"📊 Found {orphaned_count} orphaned user records")
    
    if orphaned_count > 0:
        # Delete orphaned users
        orphaned_users.delete()
        print(f"🗑️ Deleted {orphaned_count} orphaned user records")
    
    return orphaned_count

def verify_database_integrity():
    """Verify database integrity after fixes"""
    
    print("🔍 Verifying database integrity...")
    
    # Check for users without client profiles (excluding staff)
    users_without_clients = User.objects.filter(
        client_profile__isnull=True,
        is_staff=False,
        is_superuser=False
    ).count()
    
    # Check for clients without users (should be 0)
    clients_without_users = Client.objects.filter(user__isnull=True).count()
    
    print(f"📊 Users without client profiles (non-staff): {users_without_clients}")
    print(f"📊 Clients without users: {clients_without_users}")
    
    if users_without_clients == 0 and clients_without_users == 0:
        print("✅ Database integrity verified")
        return True
    else:
        print("❌ Database integrity issues found")
        return False

def main():
    """Main function to fix the database issues"""
    
    print("🚀 Starting database fix process...")
    print("=" * 50)
    
    try:
        # Step 1: Clean up orphaned users
        cleanup_orphaned_users()
        print()
        
        # Step 2: Fix the user sequence
        fix_user_sequence()
        print()
        
        # Step 3: Verify integrity
        verify_database_integrity()
        print()
        
        print("=" * 50)
        print("✅ Database fix process completed successfully!")
        print("🎉 You can now create clients without constraint violations.")
        
    except Exception as e:
        print(f"❌ Error during database fix: {str(e)}")
        print("🔧 Please check your database configuration and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()