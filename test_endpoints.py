#!/usr/bin/env python
"""
Simple test script to verify the fixed endpoints work correctly
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.development')
django.setup()

from django.test import RequestFactory
from admin_portal.v1.views.behavior_analytics import UserBehaviorPatternsView
from admin_portal.v1.views.workspace_usage import WorkspaceUsageAnalyticsView

def test_behavior_analytics():
    """Test behavior analytics endpoint"""
    try:
        factory = RequestFactory()
        request = factory.get('/admin-portal/v1/behavior-analytics/user-behavior/')
        
        view = UserBehaviorPatternsView()
        response = view.get(request)
        
        print("✅ Behavior Analytics endpoint working")
        print(f"Response status: {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ Behavior Analytics endpoint failed: {e}")
        return False

def test_workspace_usage():
    """Test workspace usage endpoint"""
    try:
        factory = RequestFactory()
        request = factory.get('/admin-portal/v1/workspace-usage/analytics/')
        
        view = WorkspaceUsageAnalyticsView()
        response = view.get(request)
        
        print("✅ Workspace Usage endpoint working")
        print(f"Response status: {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ Workspace Usage endpoint failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing fixed endpoints...")
    print("-" * 40)
    
    success_count = 0
    total_tests = 2
    
    if test_behavior_analytics():
        success_count += 1
    
    if test_workspace_usage():
        success_count += 1
    
    print("-" * 40)
    print(f"Tests passed: {success_count}/{total_tests}")
    
    if success_count == total_tests:
        print("🎉 All endpoints are working correctly!")
        sys.exit(0)
    else:
        print("⚠️  Some endpoints still have issues")
        sys.exit(1)