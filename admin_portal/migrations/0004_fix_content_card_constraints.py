# Migration to fix ContentCard field constraints causing varchar(50) errors

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_portal', '0003_fix_remaining_varchar_constraints'),
    ]

    operations = [
        # Fix ContentCard model fields that might have varchar(50) constraints
        migrations.RunSQL(
            """
            DO $$
            DECLARE
                rec RECORD;
            BEGIN
                -- Fix ContentCard table specifically
                FOR rec IN 
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_schema = 'public' 
                    AND table_name = 'admin_portal_contentcard'
                    AND data_type = 'character varying'
                    AND character_maximum_length < 500
                LOOP
                    EXECUTE format('ALTER TABLE admin_portal_contentcard ALTER COLUMN %I TYPE varchar(500)', rec.column_name);
                END LOOP;
                
                -- Fix any other CMS-related tables that might have similar issues
                FOR rec IN 
                    SELECT table_name, column_name 
                    FROM information_schema.columns 
                    WHERE table_schema = 'public' 
                    AND table_name LIKE 'admin_portal_%'
                    AND table_name IN (
                        'admin_portal_contentcard',
                        'admin_portal_processstep', 
                        'admin_portal_servicestage',
                        'admin_portal_servicepillar',
                        'admin_portal_policyitem',
                        'admin_portal_strategicadvisorypagecontent',
                        'admin_portal_operationalsystemspagecontent',
                        'admin_portal_livingsystemspagecontent'
                    )
                    AND data_type = 'character varying'
                    AND character_maximum_length < 500
                LOOP
                    EXECUTE format('ALTER TABLE %I ALTER COLUMN %I TYPE varchar(500)', rec.table_name, rec.column_name);
                END LOOP;
            END $$;
            """,
            reverse_sql="-- No reverse operation for dynamic constraint fixes"
        ),
        
        # Specifically ensure ContentCard fields are properly sized
        migrations.RunSQL(
            "ALTER TABLE admin_portal_contentcard ALTER COLUMN card_slug TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_contentcard ALTER COLUMN card_slug TYPE varchar(255);"
        ),
        
        # Ensure image_url field can handle long URLs
        migrations.RunSQL(
            "ALTER TABLE admin_portal_contentcard ALTER COLUMN image_url TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_contentcard ALTER COLUMN image_url TYPE varchar(200);"
        ),
    ]