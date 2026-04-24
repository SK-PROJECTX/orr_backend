import os
import sys
import django
from django.conf import settings
import copy
import traceback

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.production' if '--prod' in sys.argv else 'core.settings.local')
django.setup()

from modeltranslation.translator import translator
from admin_portal.models_cms import Audit
from django.db.models import JSONField, Model

def is_empty(val):
    if not val:
        return True
    if isinstance(val, dict):
        return not bool(val.get('content', '').strip())
    if isinstance(val, str):
        return not bool(val.strip())
    return False

def clone_val(val):
    if isinstance(val, dict):
        return copy.deepcopy(val)
    return val

def fix_all_empty_cms():
    print("Fixing all empty CMS content...")
    updated_count = 0
    empty_fields_found = 0

    registered_models = translator.get_registered_models()
    
    for model in registered_models:
        trans_opts = translator.get_options_for_model(model)
        if not issubclass(model, Model):
            continue

        try:
            instances = model.objects.all()
            for instance in instances:
                has_changes = False
                for field_name in trans_opts.fields:
                    field_en = f"{field_name}_en"
                    field_it = f"{field_name}_it"
                    
                    if not hasattr(instance, field_en) or not hasattr(instance, field_it):
                        continue
                        
                    val_en = getattr(instance, field_en, None)
                    val_it = getattr(instance, field_it, None)
                    val_std = getattr(instance, field_name, None)
                    
                    # Ensure base field has value if _en is missing
                    if is_empty(val_en) and not is_empty(val_std):
                        val_en = clone_val(val_std)
                        setattr(instance, field_en, val_en)
                        has_changes = True

                    # If english is missing but we have it in italian (unlikely)
                    if is_empty(val_en) and not is_empty(val_it):
                        val_en = clone_val(val_it)
                        setattr(instance, field_en, val_en)
                        has_changes = True
                    
                    # The main fix: if italian is empty but english is not
                    if is_empty(val_it) and not is_empty(val_en):
                        empty_fields_found += 1
                        setattr(instance, field_it, clone_val(val_en))
                        has_changes = True
                        print(f"[{model.__name__} {instance.pk}] Backfilled {field_it} from {field_en}")

                    # Fix standard field
                    if is_empty(val_std) and not is_empty(val_en):
                        setattr(instance, field_name, clone_val(val_en))
                        has_changes = True

                if has_changes:
                    # Update safely
                    instance.save()
                    updated_count += 1
        except Exception as e:
            print(f"Error processing {model.__name__}: {str(e)}")
            traceback.print_exc()

    print(f"[SUCCESS] Fixed {empty_fields_found} empty fields across {updated_count} CMS objects.")

if __name__ == '__main__':
    fix_all_empty_cms()
