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
import uuid

def test_client_creation_fresh():
    print("Testing fresh client creation...")
    
    # Generate unique test data
    unique_id = str(uuid.uuid4())[:8]
    test_data = {
        'username': f'newclient_{unique_id}',
        'email': f'newclient_{unique_id}@example.com',
        'full_name': f'New Client {unique_id}',
        'company': 'Test Company Inc',
        'role': 'CEO',
        'stage': 'discover',
        'primary_pillar': 'strategic'
    }
    
    print(f"Test data: {test_data}")
    
    try:
        # Test serializer validation
        serializer = ClientCreateSerializer(data=test_data)
        if not serializer.is_valid():
            print("Serializer validation failed:")
            print(serializer.errors)
            return
        
        print("[OK] Serializer validation passed")
        validated_data = serializer.validated_data
        
        # Test user creation
        user_data = {
            'username': validated_data['username'],
            'email': validated_data['email'],
        }
        
        # Handle full name parsing
        full_name = validated_data.get('full_name', '')
        if full_name:
            name_parts = full_name.strip().split()
            user_data['first_name'] = name_parts[0] if name_parts else ''
            user_data['last_name'] = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''
        
        print(f"User data: {user_data}")
        
        user = User.objects.create_user(**user_data)
        print(f"[OK] User created: {user}")
        
        # Get or create admin user
        admin_user = User.objects.filter(is_staff=True).first()
        if not admin_user:
            print("Creating admin user...")
            admin_user = User.objects.create_user(
                username='admin_test',
                email='admin@test.com',
                is_staff=True,
                is_superuser=True
            )
        
        # Test client creation
        client = Client.objects.create(
            user=user,
            company=validated_data.get('company', ''),
            role=validated_data.get('role', ''),
            stage=validated_data.get('stage', 'discover'),
            primary_pillar=validated_data.get('primary_pillar', 'strategic'),
            assigned_admin=admin_user,
        )
        
        print(f"[OK] Client created successfully: {client}")
        print(f"[OK] Client ID: {client.id}")
        print(f"[OK] Client user: {client.user.username}")
        print(f"[OK] Client company: {client.company}")
        
        # Test the response serializer
        from admin_portal.v1.serializers.client import ClientListSerializer
        response_serializer = ClientListSerializer(client)
        print(f"[OK] Response data: {response_serializer.data}")
        
        print("\n[SUCCESS] Test completed successfully!")
        
        # Clean up
        print("Cleaning up test data...")
        client.delete()
        user.delete()
        print("[OK] Cleanup completed")
        
    except Exception as e:
        print(f"[ERROR] Error during client creation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_client_creation_fresh()