#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_dir)

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.development')
django.setup()

from admin_portal.models_cms import StrategicAdvisoryPageContent

def check_details():
    page = StrategicAdvisoryPageContent.objects.filter(is_active=True).first()
    if not page:
        print("No active record")
        return
    
    print(f"ID: {page.id}")
    print(f"hero_title_en: {page.hero_title_en}")
    print(f"hero_title_it: {page.hero_title_it}")
    print(f"process_step_4_it: {page.process_step_4_it}")
    print(f"process_step_4_title_it: {page.process_step_4_title_it}")
    
    # List all fields
    print("\nAll Fields:")
    for f in page._meta.fields:
        if f.name.endswith('_it'):
            val = getattr(page, f.name)
            print(f"  {f.name}: {val}")

if __name__ == '__main__':
    check_details()
