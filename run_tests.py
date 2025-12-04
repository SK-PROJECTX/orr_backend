#!/usr/bin/env python3
"""
Test runner for ORR backend tests
"""
import subprocess
import sys
import os

def run_test(test_file, description):
    """Run a single test file"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run([sys.executable, test_file], 
                              capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode == 0:
            print("✅ PASSED")
            if result.stdout:
                print(result.stdout)
        else:
            print("❌ FAILED")
            if result.stderr:
                print("Error:", result.stderr)
            if result.stdout:
                print("Output:", result.stdout)
                
    except Exception as e:
        print(f"❌ ERROR: {e}")

def main():
    """Run all tests"""
    print("🚀 ORR Backend Test Suite")
    print("Starting comprehensive testing...")
    
    tests = [
        ("test_models_import.py", "Model Import Test"),
        ("test_auth_flow.py", "Authentication Flow Test"),
        ("test_api_fix.py", "API Endpoints Test"),
        ("test_image_upload.py", "Image Upload Test"),
        ("test_cms_integration.py", "CMS Integration Test"),
    ]
    
    for test_file, description in tests:
        if os.path.exists(test_file):
            run_test(test_file, description)
        else:
            print(f"\n❌ Test file not found: {test_file}")
    
    print(f"\n{'='*60}")
    print("🎉 Test Suite Complete!")
    print("📝 To run individual tests:")
    for test_file, _ in tests:
        print(f"   python {test_file}")
    print("📝 To run Django tests:")
    print("   python manage.py test")

if __name__ == "__main__":
    main()