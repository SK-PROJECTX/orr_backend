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

def debug_all():
    models = [
        ("Strategic Advisory", StrategicAdvisoryPageContent),
        ("Operational Systems", OperationalSystemsPageContent),
        ("Living Systems", LivingSystemsPageContent),
        ("How We Operate", HowWeOperatePageContent)
    ]
    
    for name, model in models:
        print(f"\n--- {name} ---")
        page = model.objects.filter(is_active=True).first()
        if not page:
            print("No active record")
            continue
        print(f"ID: {page.id}")
        for f in sorted([f.name for f in page._meta.fields if f.name.endswith('_it')]):
            val = getattr(page, f)
            print(f"  {f}: {val}")

if __name__ == '__main__':
    debug_all()
