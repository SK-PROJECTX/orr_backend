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
from admin_portal.v1.serializers.client import ClientCreateSerializer

def test_client_creation():
    print("Testing client creation...")
    
    # Test data
    test_data = {
        'username': 'testuser123',
        'email': 'test@example.com',
        'full_name': 'Test User',
        'company': 'Test Company',
        'role': 'Manager',
        'stage': 'discover',
        'primary_pillar': 'strategic'
    }
    
    try:
        # Test serializer validation
        serializer = ClientCreateSerializer(data=test_data)
        if not serializer.is_valid():
            print("Serializer validation failed:")
            print(serializer.errors)
            return
        
        print("Serializer validation passed")
        validated_data = serializer.validated_data
        print(f"Validated data: {validated_data}")
        
        # Test user creation
        user_data = {
            'username': validated_data['username'],
            'email': validated_data['email'],
            'first_name': validated_data.get('full_name', '').split(' ')[0] if validated_data.get('full_name') else '',
            'last_name': ' '.join(validated_data.get('full_name', '').split(' ')[1:]) if validated_data.get('full_name') and len(validated_data.get('full_name', '').split(' ')) > 1 else '',
        }
        
        print(f"User data: {user_data}")
        
        # Check if user already exists
        if User.objects.filter(username=user_data['username']).exists():
            print("User already exists, deleting...")
            User.objects.filter(username=user_data['username']).delete()
        
        user = User.objects.create_user(**user_data)
        print(f"User created: {user}")
        
        # Test client creation
        # Get a test admin user
        admin_user = User.objects.filter(is_staff=True).first()
        if not admin_user:
            print("No admin user found, creating one...")
            admin_user = User.objects.create_user(
                username='admin_test',
                email='admin@test.com',
                is_staff=True,
                is_superuser=True
            )
        
        client = Client.objects.create(
            user=user,
            company=validated_data.get('company', ''),
            role=validated_data.get('role', ''),
            stage=validated_data.get('stage', 'discover'),
            primary_pillar=validated_data.get('primary_pillar', 'strategic'),
            assigned_admin=admin_user,
        )
        
        print(f"Client created successfully: {client}")
        print(f"Client ID: {client.id}")
        
        # Clean up
        client.delete()
        user.delete()
        
        print("Test completed successfully!")
        
    except Exception as e:
        print(f"Error during client creation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_client_creation()