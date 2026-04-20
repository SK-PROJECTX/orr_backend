import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from admin_portal.models_cms import (
    ApproachSection, BusinessSystemSection, ORRRoleSection, 
    MessageStrip, ORRReportSection, ServiceCard, ContactPage
)

def verify_translations():
    print("Verifying Italian translations in database...")
    
    models_to_check = [
        (ApproachSection, 'title_it'),
        (BusinessSystemSection, 'title_it'),
        (ORRRoleSection, 'title_it'),
        (MessageStrip, 'message_it'),
        (ORRReportSection, 'title_it'),
        (ContactPage, 'hero_title_it')
    ]
    
    all_ok = True
    for model, field in models_to_check:
        obj = model.objects.filter(is_active=True).first()
        if obj:
            val = getattr(obj, field, None)
            display_val = ""
            if isinstance(val, dict) and 'content' in val:
                display_val = val['content']
            elif isinstance(val, str):
                display_val = val
                
            if display_val:
                print(f"[OK] {model.__name__} has Italian translation: {display_val[:50]}...")
            else:
                print(f"[FAIL] {model.__name__} is missing Italian translation in {field}")
                all_ok = False
        else:
            print(f"[SKIP] {model.__name__} has no active instance to check")
            
    if all_ok:
        print("\nAll checked models have Italian translations populated!")
    else:
        print("\nSome translations are missing.")

if __name__ == '__main__':
    verify_translations()
