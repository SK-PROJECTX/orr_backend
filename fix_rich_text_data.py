#!/usr/bin/env python
"""
Script to convert all plain text fields to rich text JSON format in the database
Run this before applying the rich text migrations
"""

import os
import django
import json
from django.db import connection

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.development')
django.setup()

def escape_json_string(text):
    """Escape quotes and other characters for JSON"""
    if not text:
        return text
    return text.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t')

def convert_text_fields():
    """Convert all plain text fields to JSON format"""
    
    cursor = connection.cursor()
    
    # List of tables and their text fields that need conversion
    tables_fields = {
        'admin_portal_homepage': [
            'hero_title', 'hero_subtitle', 'hero_cta_text', 'about_title', 'about_content',
            'services_title', 'services_subtitle', 'service_1_title', 'service_1_description',
            'service_1_button', 'service_2_title', 'service_2_description', 'service_2_button',
            'service_3_title', 'service_3_description', 'service_3_button', 'contact_title',
            'contact_subtitle', 'meta_title', 'meta_description'
        ],
        'admin_portal_approachsection': [
            'title', 'paragraph_1', 'paragraph_2', 'paragraph_3'
        ],
        'admin_portal_messagestrip': [
            'title', 'message'
        ],
        'admin_portal_sitesettings': [
            'site_name', 'site_tagline', 'footer_text', 'copyright_text'
        ],
        'admin_portal_testimonial': [
            'client_name', 'client_company', 'client_role', 'testimonial_text'
        ]
    }
    
    for table_name, field_names in tables_fields.items():
        print(f"Processing table: {table_name}")
        
        try:
            # Check if table exists
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"  Found {count} records")
            
            if count == 0:
                continue
                
            for field_name in field_names:
                try:
                    # Update fields that are not already JSON
                    sql = f"""
                    UPDATE {table_name} 
                    SET {field_name} = %s
                    WHERE {field_name} IS NOT NULL 
                    AND {field_name} != '' 
                    AND {field_name} NOT LIKE '{{%'
                    """
                    
                    # Get current values
                    cursor.execute(f"SELECT id, {field_name} FROM {table_name} WHERE {field_name} IS NOT NULL AND {field_name} != '' AND {field_name} NOT LIKE '{{%'")
                    rows = cursor.fetchall()
                    
                    for row_id, current_value in rows:
                        if current_value and isinstance(current_value, str):
                            # Create JSON format
                            json_value = json.dumps({
                                'content': current_value,
                                'format': 'html'
                            })
                            
                            # Update the specific row
                            cursor.execute(f"UPDATE {table_name} SET {field_name} = %s WHERE id = %s", [json_value, row_id])
                            print(f"    Updated {field_name} for record {row_id}")
                    
                except Exception as e:
                    print(f"    Error processing field {field_name}: {e}")
                    continue
                    
        except Exception as e:
            print(f"  Error processing table {table_name}: {e}")
            continue
    
    print("Conversion completed!")

if __name__ == "__main__":
    convert_text_fields()