#!/usr/bin/env python
"""
Script to apply database migrations and fix varchar(50) constraints
"""

import os
import sys
import django

# Add the project directory to the Python path
sys.path.append('/orr')

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.production')

# Setup Django
django.setup()

from django.core.management import execute_from_command_line
from django.db import connection

def main():
    """Apply migrations and fix database constraints"""
    
    print("Starting database migration and constraint fixes...")
    
    try:
        # Make migrations for admin_portal
        print("Creating migrations...")
        execute_from_command_line(['manage.py', 'makemigrations', 'admin_portal'])
        
        # Apply migrations
        print("Applying migrations...")
        execute_from_command_line(['manage.py', 'migrate'])
        
        print("Database migrations completed successfully!")
        
        # Check for any remaining varchar(50) constraints
        print("Checking for remaining varchar(50) constraints...")
        
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT table_name, column_name, character_maximum_length
                FROM information_schema.columns 
                WHERE table_schema = 'public' 
                AND table_name LIKE 'admin_portal_%'
                AND data_type = 'character varying'
                AND character_maximum_length = 50
            """)
            
            remaining_constraints = cursor.fetchall()
            
            if remaining_constraints:
                print(f"Found {len(remaining_constraints)} remaining varchar(50) constraints:")
                for table, column, length in remaining_constraints:
                    print(f"  - {table}.{column} (length: {length})")
                    
                    # Fix each remaining constraint
                    try:
                        cursor.execute(f"ALTER TABLE {table} ALTER COLUMN {column} TYPE varchar(500)")
                        print(f"    Fixed: {table}.{column}")
                    except Exception as e:
                        print(f"    Error fixing {table}.{column}: {e}")
            else:
                print("No remaining varchar(50) constraints found!")
        
        print("All database constraint fixes completed!")
        
    except Exception as e:
        print(f"Error during migration: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()