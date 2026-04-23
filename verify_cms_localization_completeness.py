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

from admin_portal.models_cms import (
    StrategicAdvisoryPageContent, OperationalSystemsPageContent, 
    LivingSystemsPageContent, HowWeOperatePageContent
)

def verify_localization(page_name, model_class):
    print(f"\n--- Verifying {page_name} ---")
    page = model_class.objects.filter(is_active=True).first()
    if not page:
        print("x No active record found")
        return
    
    # Get all fields that end with _en or _it
    fields = [f.name for f in page._meta.fields]
    en_fields = sorted([f for f in fields if f.endswith('_en')])
    
    missing_it = []
    for en_f in en_fields:
        it_f = en_f.replace('_en', '_it')
        en_val = getattr(page, en_f)
        it_val = getattr(page, it_f)
        
        # Check if it_val is "empty"
        is_empty = False
        if it_val is None:
            is_empty = True
        elif isinstance(it_val, str) and not it_val.strip():
            is_empty = True
        elif isinstance(it_val, dict) and not it_val.get('content', '').strip():
            is_empty = True
        
        if is_empty:
            missing_it.append(it_f)
        else:
            print(f"  [OK] {it_f}")
            
    if missing_it:
        print(f"  [MISSING IT] {len(missing_it)} fields: {', '.join(missing_it)}")
    else:
        print("  [ALL IT LOADED]")

if __name__ == '__main__':
    verify_localization("Strategic Advisory", StrategicAdvisoryPageContent)
    verify_localization("Operational Systems", OperationalSystemsPageContent)
    verify_localization("Living Systems", LivingSystemsPageContent)
    verify_localization("How We Operate", HowWeOperatePageContent)
