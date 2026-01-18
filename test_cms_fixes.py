#!/usr/bin/env python
"""
Test script to verify CMS fixes for varchar(50) constraint issues.
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.insert(0, os.getcwd())

# Setup Django environment with development settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.development')
django.setup()

from admin_portal.models_cms import ContentCard
from admin_portal.cms_utils import CMSFieldValidator, validate_and_clean_cms_data, CMSValidationError


def run_manual_tests():
    """Run manual tests to verify fixes"""
    print("Running manual CMS fixes tests...")
    
    # Test 1: Create ContentCard with long content
    print("\n1. Testing ContentCard creation with long content...")
    try:
        long_title = 'Test Title ' + 'X' * 100
        card = ContentCard.objects.create(
            badge={'content': 'Test Badge', 'format': 'html'},
            title={'content': long_title, 'format': 'html'},
            content=['Test content with reasonable length'],
            image_url='https://example.com/test-image.jpg',
            is_active=True
        )
        print(f"✓ Successfully created ContentCard with ID: {card.id}")
        print(f"  Title length: {len(card.title['content'])} characters")
        
        # Clean up
        card.delete()
        
    except Exception as e:
        print(f"✗ Failed to create ContentCard: {e}")
    
    # Test 2: Test field validator
    print("\n2. Testing CMS field validator...")
    try:
        # Test valid data
        valid_data = {
            'title': {'content': 'Valid Title', 'format': 'html'},
            'badge': {'content': 'Valid Badge', 'format': 'html'},
        }
        validated = CMSFieldValidator.validate_content_card_data(valid_data)
        print("✓ Valid data passed validation")
        
        # Test invalid data
        invalid_data = {
            'title': {'content': 'A' * 3000, 'format': 'html'},
        }
        try:
            CMSFieldValidator.validate_content_card_data(invalid_data)
            print("✗ Invalid data should have failed validation")
        except CMSValidationError:
            print("✓ Invalid data correctly failed validation")
            
    except Exception as e:
        print(f"✗ Field validator test failed: {e}")
    
    # Test 3: Test data cleaning
    print("\n3. Testing data cleaning function...")
    try:
        messy_data = {
            'title': {'content': 'A' * 3000, 'format': 'html'},  # Too long
            'badge': {'content': 'Valid Badge', 'format': 'html'},
            'image_url': 'https://example.com/image.jpg',
        }
        
        cleaned = validate_and_clean_cms_data(messy_data, "content_card")
        print("✓ Data cleaning completed successfully")
        print(f"  Original title length: {len(messy_data['title']['content'])}")
        print(f"  Cleaned title length: {len(cleaned['title']['content'])}")
        
    except Exception as e:
        print(f"✗ Data cleaning test failed: {e}")
    
    print("\nManual tests completed.")


if __name__ == '__main__':
    run_manual_tests()