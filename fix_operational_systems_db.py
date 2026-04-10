#!/usr/bin/env python
"""
Script to fix missing database columns for OperationalSystemsPageContent
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.production')
django.setup()

from django.db import connection

def fix_operational_systems_columns():
    """Add missing columns to OperationalSystemsPageContent table"""
    
    print("Checking and fixing OperationalSystemsPageContent table...")
    
    with connection.cursor() as cursor:
        # Check if the table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'admin_portal_operationalsystemspagecontent'
            );
        """)
        
        table_exists = cursor.fetchone()[0]
        
        if not table_exists:
            print("❌ Table admin_portal_operationalsystemspagecontent does not exist")
            print("Please run: python manage.py makemigrations admin_portal")
            print("Then run: python manage.py migrate")
            return
        
        # List of columns that should exist
        required_columns = [
            'process_step_1_title',
            'process_step_2_title', 
            'process_step_3_title',
            'process_step_4_title'
        ]
        
        for column in required_columns:
            # Check if column exists
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.columns 
                    WHERE table_name = 'admin_portal_operationalsystemspagecontent' 
                    AND column_name = %s
                );
            """, [column])
            
            column_exists = cursor.fetchone()[0]
            
            if not column_exists:
                print(f"➕ Adding missing column: {column}")
                cursor.execute(f"""
                    ALTER TABLE admin_portal_operationalsystemspagecontent 
                    ADD COLUMN {column} TEXT DEFAULT '';
                """)
            else:
                print(f"✅ Column {column} already exists")
    
    print("\n✅ Database schema fix completed!")
    print("The operational systems API should now work correctly.")

if __name__ == '__main__':
    fix_operational_systems_columns()