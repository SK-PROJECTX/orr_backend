# Migration to fix remaining character varying(50) constraints

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_portal', '0002_fix_production_constraints'),
    ]

    operations = [
        # Fix any remaining varchar(50) constraints that might be causing issues
        
        # ContentCard model - ensure all text fields can handle longer content
        migrations.RunSQL(
            "ALTER TABLE admin_portal_contentcard ALTER COLUMN card_slug TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_contentcard ALTER COLUMN card_slug TYPE varchar(255);"
        ),
        
        # Check if there are any other fields that might have varchar(50) constraints
        # These are common fields that might cause issues:
        
        # Testimonial fields
        migrations.RunSQL(
            "ALTER TABLE admin_portal_testimonial ALTER COLUMN client_photo TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_testimonial ALTER COLUMN client_photo TYPE varchar(100);"
        ),
        
        # BlogPost fields
        migrations.RunSQL(
            "ALTER TABLE admin_portal_blogpost ALTER COLUMN featured_image TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_blogpost ALTER COLUMN featured_image TYPE varchar(100);"
        ),
        
        # HomePage image fields
        migrations.RunSQL(
            "ALTER TABLE admin_portal_homepage ALTER COLUMN hero_background_image TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_homepage ALTER COLUMN hero_background_image TYPE varchar(100);"
        ),
        migrations.RunSQL(
            "ALTER TABLE admin_portal_homepage ALTER COLUMN about_image TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_homepage ALTER COLUMN about_image TYPE varchar(100);"
        ),
        
        # BusinessSystemCard fields
        migrations.RunSQL(
            "ALTER TABLE admin_portal_businesssystemcard ALTER COLUMN image TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_businesssystemcard ALTER COLUMN image TYPE varchar(100);"
        ),
        
        # BusinessSystemSection image fields
        migrations.RunSQL(
            "ALTER TABLE admin_portal_businesssystemsection ALTER COLUMN card_1_image TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_businesssystemsection ALTER COLUMN card_1_image TYPE varchar(100);"
        ),
        migrations.RunSQL(
            "ALTER TABLE admin_portal_businesssystemsection ALTER COLUMN card_2_image TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_businesssystemsection ALTER COLUMN card_2_image TYPE varchar(100);"
        ),
        migrations.RunSQL(
            "ALTER TABLE admin_portal_businesssystemsection ALTER COLUMN card_3_image TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_businesssystemsection ALTER COLUMN card_3_image TYPE varchar(100);"
        ),
        
        # SiteSettings image fields
        migrations.RunSQL(
            "ALTER TABLE admin_portal_sitesettings ALTER COLUMN logo TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_sitesettings ALTER COLUMN logo TYPE varchar(100);"
        ),
        migrations.RunSQL(
            "ALTER TABLE admin_portal_sitesettings ALTER COLUMN favicon TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_sitesettings ALTER COLUMN favicon TYPE varchar(100);"
        ),
        
        # Ensure all RichTextField content fields can handle long content
        # These might be stored as TEXT but let's make sure they're not constrained
        
        # Add any other fields that might be causing varchar(50) constraint issues
        # We'll use a more comprehensive approach to catch any remaining issues
        
        # Fix any remaining fields that might have been missed
        migrations.RunSQL(
            """
            DO $$
            DECLARE
                rec RECORD;
            BEGIN
                FOR rec IN 
                    SELECT table_name, column_name 
                    FROM information_schema.columns 
                    WHERE table_schema = 'public' 
                    AND table_name LIKE 'admin_portal_%'
                    AND data_type = 'character varying'
                    AND character_maximum_length = 50
                LOOP
                    EXECUTE format('ALTER TABLE %I ALTER COLUMN %I TYPE varchar(500)', rec.table_name, rec.column_name);
                END LOOP;
            END $$;
            """,
            reverse_sql="-- No reverse operation for dynamic constraint fixes"
        ),
    ]