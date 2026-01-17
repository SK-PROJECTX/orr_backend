# Generated migration to fix rich text data before schema changes

from django.db import migrations
import json


# Generated migration to fix rich text data before schema changes

from django.db import migrations
import json


# Generated migration to fix rich text data before schema changes

from django.db import migrations
import json


def convert_plain_text_to_rich_format(apps, schema_editor):
    """Convert any plain text fields to rich text JSON format"""
    
    # Only handle the most critical models first
    models_fields = {
        'ApproachSection': ['paragraph_1', 'paragraph_2', 'paragraph_3', 'title'],
    }
    
    for model_name, field_names in models_fields.items():
        try:
            Model = apps.get_model('admin_portal', model_name)
            
            for instance in Model.objects.all():
                updated = False
                
                for field_name in field_names:
                    if hasattr(instance, field_name):
                        value = getattr(instance, field_name)
                        
                        # If it's a string (plain text), convert to rich text format
                        if isinstance(value, str) and value.strip():
                            try:
                                # Try to parse as JSON first
                                json.loads(value)
                                # If it's already JSON, skip
                                continue
                            except (json.JSONDecodeError, ValueError):
                                # Not JSON, convert to rich text format
                                rich_value = {
                                    'content': value,
                                    'format': 'html'
                                }
                                setattr(instance, field_name, rich_value)
                                updated = True
                
                if updated:
                    try:
                        instance.save()
                        print(f"Updated {model_name} instance {instance.id}")
                    except Exception as e:
                        print(f"Failed to save {model_name} instance {instance.id}: {e}")
                        continue
                    
        except Exception as e:
            print(f"Skipping {model_name}: {e}")
            continue


def reverse_rich_text_to_plain(apps, schema_editor):
    """Reverse operation - convert rich text back to plain text"""
    
    models_fields = {
        'ApproachSection': ['paragraph_1', 'paragraph_2', 'paragraph_3', 'title'],
    }
    
    for model_name, field_names in models_fields.items():
        try:
            Model = apps.get_model('admin_portal', model_name)
            
            for instance in Model.objects.all():
                updated = False
                
                for field_name in field_names:
                    if hasattr(instance, field_name):
                        value = getattr(instance, field_name)
                        
                        # If it's a dict with content, extract the content
                        if isinstance(value, dict) and 'content' in value:
                            setattr(instance, field_name, value['content'])
                            updated = True
                
                if updated:
                    try:
                        instance.save()
                    except Exception as e:
                        print(f"Failed to reverse {model_name} instance {instance.id}: {e}")
                        continue
                    
        except Exception as e:
            print(f"Skipping {model_name}: {e}")
            continue


class Migration(migrations.Migration):

    dependencies = [
        ('admin_portal', '0023_alter_operationalsystemspagecontent_process_step_1_title_and_more'),
    ]

    operations = [
        migrations.RunPython(
            convert_plain_text_to_rich_format,
            reverse_rich_text_to_plain
        ),
    ]