#!/usr/bin/env python3
"""
Test script to verify models can be imported correctly
"""
import os
import sys
import django

# Change to the Django project directory
os.chdir('orr')

# Add the project directory to Python path
sys.path.insert(0, os.getcwd())

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.base')
django.setup()

try:
    print("Testing model imports...")
    
    # Test importing from models_cms
    from admin_portal.models_cms import (
        HomePage,
        ServiceCard,
        Testimonial,
        FAQ,
        BlogPost,
        ContactInfo,
        SiteSettings,
        ApproachSection,
        BusinessSystemCard,
        BusinessSystemSection,
        ORRRoleSection,
        MessageStrip,
        ProcessStage,
        ProcessSection,
        ORRReportSection,
    )
    print("[SUCCESS] Successfully imported all CMS models")
    
    # Test creating a BusinessSystemSection instance
    section = BusinessSystemSection()
    print(f"[SUCCESS] BusinessSystemSection instance created: {section}")
    
    # Test the model fields
    print(f"[SUCCESS] Default title: {section.title}")
    print(f"[SUCCESS] Default subtitle: {section.subtitle}")
    
    print("\n[SUCCESS] All model imports and basic functionality working correctly!")
    
except Exception as e:
    print(f"[ERROR] Error importing models: {e}")
    import traceback
    traceback.print_exc()

if __name__ == "__main__":
    pass