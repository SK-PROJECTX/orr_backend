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
from admin_portal.models import AdminRole, AdminProfile

def create_test_admin():
    print("Creating test admin user...")
    
    # Create or get admin user
    username = "testadmin"
    password = "testpass123"
    
    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            'email': 'testadmin@example.com',
            'is_staff': True,
            'is_superuser': True,
            'first_name': 'Test',
            'last_name': 'Admin'
        }
    )
    
    if created:
        user.set_password(password)
        user.save()
        print(f"Created new admin user: {username}")
    else:
        # Update password in case it was different
        user.set_password(password)
        user.save()
        print(f"Updated existing admin user: {username}")
    
    # Create admin role if it doesn't exist
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
    
    # Create admin profile if it doesn't exist
    admin_profile, created = AdminProfile.objects.get_or_create(
        user=user,
        defaults={
            'role': admin_role,
            'department': 'IT',
            'is_active': True
        }
    )
    
    if created:
        print(f"Created admin profile for {username}")
    else:
        print(f"Admin profile already exists for {username}")
    
    print(f"Test admin credentials:")
    print(f"Username: {username}")
    print(f"Password: {password}")

if __name__ == '__main__':
    create_test_admin()