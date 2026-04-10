#!/usr/bin/env python
import os
import sys
import django
from django.urls import get_resolver
from django.conf import settings

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

def print_url_patterns(urlpatterns, prefix=''):
    """Recursively print all URL patterns"""
    for pattern in urlpatterns:
        if hasattr(pattern, 'url_patterns'):
            # This is an include() pattern
            print(f"{prefix}{pattern.pattern} -> INCLUDE")
            print_url_patterns(pattern.url_patterns, prefix + "  ")
        else:
            # This is a regular pattern
            if hasattr(pattern, 'name') and pattern.name:
                print(f"{prefix}{pattern.pattern} -> {pattern.name}")
            else:
                print(f"{prefix}{pattern.pattern}")

def main():
    print("Django URL Patterns Debug")
    print("=" * 50)
    print(f"Settings module: {settings.SETTINGS_MODULE}")
    print(f"Debug mode: {settings.DEBUG}")
    print("=" * 50)
    
    # Get the root URL resolver
    resolver = get_resolver()
    
    print("All URL patterns:")
    print_url_patterns(resolver.url_patterns)
    
    print("\n" + "=" * 50)
    print("Looking for billing patterns specifically:")
    
    # Look for billing patterns
    found_billing = False
    for pattern in resolver.url_patterns:
        if 'admin-portal' in str(pattern.pattern):
            print(f"Found admin-portal pattern: {pattern.pattern}")
            if hasattr(pattern, 'url_patterns'):
                for sub_pattern in pattern.url_patterns:
                    if 'v1' in str(sub_pattern.pattern):
                        print(f"  Found v1 pattern: {sub_pattern.pattern}")
                        if hasattr(sub_pattern, 'url_patterns'):
                            for v1_pattern in sub_pattern.url_patterns:
                                if 'billing' in str(v1_pattern.pattern):
                                    print(f"    Found billing pattern: {v1_pattern.pattern}")
                                    found_billing = True
    
    if not found_billing:
        print("No billing patterns found!")
    
    # Test URL resolution
    print("\n" + "=" * 50)
    print("Testing URL resolution:")
    
    from django.urls import resolve, reverse
    
    test_urls = [
        '/admin-portal/v1/billing-history/stats/',
        '/admin-portal/v1/billing-history/',
    ]
    
    for url in test_urls:
        try:
            match = resolve(url)
            print(f"[OK] {url} -> {match.func.__name__} ({match.view_name})")
        except Exception as e:
            print(f"[ERROR] {url} -> ERROR: {e}")
    
    # Test reverse lookup
    print("\nTesting reverse lookup:")
    try:
        stats_url = reverse('admin-billing-stats')
        history_url = reverse('admin-billing-history')
        print(f"[OK] admin-billing-stats -> {stats_url}")
        print(f"[OK] admin-billing-history -> {history_url}")
    except Exception as e:
        print(f"[ERROR] Reverse lookup failed: {e}")

if __name__ == "__main__":
    main()