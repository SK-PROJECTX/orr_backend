# Migration to fix character varying(50) constraints

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_portal', '0001_initial'),
    ]

    operations = [
        # HomePage fields
        migrations.RunSQL(
            "ALTER TABLE admin_portal_homepage ALTER COLUMN hero_cta_link TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_homepage ALTER COLUMN hero_cta_link TYPE varchar(200);"
        ),
        migrations.RunSQL(
            "ALTER TABLE admin_portal_homepage ALTER COLUMN services_glow_image TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_homepage ALTER COLUMN services_glow_image TYPE varchar(500);"
        ),
        migrations.RunSQL(
            "ALTER TABLE admin_portal_homepage ALTER COLUMN contact_email TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_homepage ALTER COLUMN contact_email TYPE varchar(254);"
        ),
        migrations.RunSQL(
            "ALTER TABLE admin_portal_homepage ALTER COLUMN contact_phone TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_homepage ALTER COLUMN contact_phone TYPE varchar(20);"
        ),
        
        # ServiceCard fields
        migrations.RunSQL(
            "ALTER TABLE admin_portal_servicecard ALTER COLUMN icon TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_servicecard ALTER COLUMN icon TYPE varchar(50);"
        ),
        migrations.RunSQL(
            "ALTER TABLE admin_portal_servicecard ALTER COLUMN pillar TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_servicecard ALTER COLUMN pillar TYPE varchar(20);"
        ),
        migrations.RunSQL(
            "ALTER TABLE admin_portal_servicecard ALTER COLUMN link TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_servicecard ALTER COLUMN link TYPE varchar(200);"
        ),
        
        # ContactInfo fields
        migrations.RunSQL(
            "ALTER TABLE admin_portal_contactinfo ALTER COLUMN postal_code TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_contactinfo ALTER COLUMN postal_code TYPE varchar(20);"
        ),
        migrations.RunSQL(
            "ALTER TABLE admin_portal_contactinfo ALTER COLUMN phone TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_contactinfo ALTER COLUMN phone TYPE varchar(20);"
        ),
        migrations.RunSQL(
            "ALTER TABLE admin_portal_contactinfo ALTER COLUMN email TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_contactinfo ALTER COLUMN email TYPE varchar(254);"
        ),
        migrations.RunSQL(
            "ALTER TABLE admin_portal_contactinfo ALTER COLUMN website TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_contactinfo ALTER COLUMN website TYPE varchar(200);"
        ),
        migrations.RunSQL(
            "ALTER TABLE admin_portal_contactinfo ALTER COLUMN linkedin_url TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_contactinfo ALTER COLUMN linkedin_url TYPE varchar(200);"
        ),
        migrations.RunSQL(
            "ALTER TABLE admin_portal_contactinfo ALTER COLUMN twitter_url TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_contactinfo ALTER COLUMN twitter_url TYPE varchar(200);"
        ),
        migrations.RunSQL(
            "ALTER TABLE admin_portal_contactinfo ALTER COLUMN facebook_url TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_contactinfo ALTER COLUMN facebook_url TYPE varchar(200);"
        ),
        migrations.RunSQL(
            "ALTER TABLE admin_portal_contactinfo ALTER COLUMN instagram_url TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_contactinfo ALTER COLUMN instagram_url TYPE varchar(200);"
        ),
        
        # FAQ fields
        migrations.RunSQL(
            "ALTER TABLE admin_portal_faq ALTER COLUMN category TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_faq ALTER COLUMN category TYPE varchar(20);"
        ),
        
        # BlogPost fields
        migrations.RunSQL(
            "ALTER TABLE admin_portal_blogpost ALTER COLUMN slug TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_blogpost ALTER COLUMN slug TYPE varchar(50);"
        ),
        migrations.RunSQL(
            "ALTER TABLE admin_portal_blogpost ALTER COLUMN status TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_blogpost ALTER COLUMN status TYPE varchar(20);"
        ),
        
        # MessageStrip fields
        migrations.RunSQL(
            "ALTER TABLE admin_portal_messagestrip ALTER COLUMN user_image_1 TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_messagestrip ALTER COLUMN user_image_1 TYPE varchar(500);"
        ),
        migrations.RunSQL(
            "ALTER TABLE admin_portal_messagestrip ALTER COLUMN user_image_2 TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_messagestrip ALTER COLUMN user_image_2 TYPE varchar(500);"
        ),
        migrations.RunSQL(
            "ALTER TABLE admin_portal_messagestrip ALTER COLUMN user_image_3 TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_messagestrip ALTER COLUMN user_image_3 TYPE varchar(500);"
        ),
        migrations.RunSQL(
            "ALTER TABLE admin_portal_messagestrip ALTER COLUMN user_image_4 TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_messagestrip ALTER COLUMN user_image_4 TYPE varchar(500);"
        ),
        
        # ORRReportSection fields
        migrations.RunSQL(
            "ALTER TABLE admin_portal_orrreportsection ALTER COLUMN feature_1_image TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_orrreportsection ALTER COLUMN feature_1_image TYPE varchar(500);"
        ),
        migrations.RunSQL(
            "ALTER TABLE admin_portal_orrreportsection ALTER COLUMN feature_2_image TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_orrreportsection ALTER COLUMN feature_2_image TYPE varchar(500);"
        ),
        migrations.RunSQL(
            "ALTER TABLE admin_portal_orrreportsection ALTER COLUMN feature_3_image TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_orrreportsection ALTER COLUMN feature_3_image TYPE varchar(500);"
        ),
        migrations.RunSQL(
            "ALTER TABLE admin_portal_orrreportsection ALTER COLUMN feature_4_image TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_orrreportsection ALTER COLUMN feature_4_image TYPE varchar(500);"
        ),
        migrations.RunSQL(
            "ALTER TABLE admin_portal_orrreportsection ALTER COLUMN main_image TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_orrreportsection ALTER COLUMN main_image TYPE varchar(500);"
        ),
        
        # ServicesPage fields
        migrations.RunSQL(
            "ALTER TABLE admin_portal_servicespage ALTER COLUMN business_gp_image TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_servicespage ALTER COLUMN business_gp_image TYPE varchar(500);"
        ),
        migrations.RunSQL(
            "ALTER TABLE admin_portal_servicespage ALTER COLUMN service_1_image TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_servicespage ALTER COLUMN service_1_image TYPE varchar(500);"
        ),
        migrations.RunSQL(
            "ALTER TABLE admin_portal_servicespage ALTER COLUMN service_2_image TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_servicespage ALTER COLUMN service_2_image TYPE varchar(500);"
        ),
        migrations.RunSQL(
            "ALTER TABLE admin_portal_servicespage ALTER COLUMN data_intelligence_image TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_servicespage ALTER COLUMN data_intelligence_image TYPE varchar(500);"
        ),
        
        # ProcessStep fields
        migrations.RunSQL(
            "ALTER TABLE admin_portal_processstep ALTER COLUMN step_number TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_processstep ALTER COLUMN step_number TYPE varchar(10);"
        ),
        migrations.RunSQL(
            "ALTER TABLE admin_portal_processstep ALTER COLUMN image_url TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_processstep ALTER COLUMN image_url TYPE varchar(200);"
        ),
        
        # ServicesPageContent fields
        migrations.RunSQL(
            "ALTER TABLE admin_portal_servicespagecontent ALTER COLUMN business_gp_image TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_servicespagecontent ALTER COLUMN business_gp_image TYPE varchar(500);"
        ),
        
        # ContentCard fields
        migrations.RunSQL(
            "ALTER TABLE admin_portal_contentcard ALTER COLUMN card_slug TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_contentcard ALTER COLUMN card_slug TYPE varchar(255);"
        ),
        migrations.RunSQL(
            "ALTER TABLE admin_portal_contentcard ALTER COLUMN image_url TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_contentcard ALTER COLUMN image_url TYPE varchar(200);"
        ),
        
        # PolicyItem fields
        migrations.RunSQL(
            "ALTER TABLE admin_portal_policyitem ALTER COLUMN number TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_policyitem ALTER COLUMN number TYPE varchar(10);"
        ),
        
        # ContactPageContent fields
        migrations.RunSQL(
            "ALTER TABLE admin_portal_contactpagecontent ALTER COLUMN phone_number TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_contactpagecontent ALTER COLUMN phone_number TYPE varchar(50);"
        ),
        migrations.RunSQL(
            "ALTER TABLE admin_portal_contactpagecontent ALTER COLUMN email_address TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_contactpagecontent ALTER COLUMN email_address TYPE varchar(254);"
        ),
        
        # ContactPage fields
        migrations.RunSQL(
            "ALTER TABLE admin_portal_contactpage ALTER COLUMN phone_number TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_contactpage ALTER COLUMN phone_number TYPE varchar(50);"
        ),
        migrations.RunSQL(
            "ALTER TABLE admin_portal_contactpage ALTER COLUMN email_address TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_contactpage ALTER COLUMN email_address TYPE varchar(254);"
        ),
        
        # LegacyPolicyPage fields
        migrations.RunSQL(
            "ALTER TABLE admin_portal_legacypolicypage ALTER COLUMN policy_item_1_number TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_legacypolicypage ALTER COLUMN policy_item_1_number TYPE varchar(10);"
        ),
        migrations.RunSQL(
            "ALTER TABLE admin_portal_legacypolicypage ALTER COLUMN policy_item_2_number TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_legacypolicypage ALTER COLUMN policy_item_2_number TYPE varchar(10);"
        ),
        migrations.RunSQL(
            "ALTER TABLE admin_portal_legacypolicypage ALTER COLUMN policy_item_3_number TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_legacypolicypage ALTER COLUMN policy_item_3_number TYPE varchar(10);"
        ),
        
        # ResourcesBlogsPage fields
        migrations.RunSQL(
            "ALTER TABLE admin_portal_resourcesblogspage ALTER COLUMN blog_card_1_image TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_resourcesblogspage ALTER COLUMN blog_card_1_image TYPE varchar(500);"
        ),
        migrations.RunSQL(
            "ALTER TABLE admin_portal_resourcesblogspage ALTER COLUMN blog_card_2_image TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_resourcesblogspage ALTER COLUMN blog_card_2_image TYPE varchar(500);"
        ),
        migrations.RunSQL(
            "ALTER TABLE admin_portal_resourcesblogspage ALTER COLUMN blog_card_3_image TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_resourcesblogspage ALTER COLUMN blog_card_3_image TYPE varchar(500);"
        ),
        migrations.RunSQL(
            "ALTER TABLE admin_portal_resourcesblogspage ALTER COLUMN blog_card_4_image TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_resourcesblogspage ALTER COLUMN blog_card_4_image TYPE varchar(500);"
        ),
        migrations.RunSQL(
            "ALTER TABLE admin_portal_resourcesblogspage ALTER COLUMN tip_1_number TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_resourcesblogspage ALTER COLUMN tip_1_number TYPE varchar(10);"
        ),
        migrations.RunSQL(
            "ALTER TABLE admin_portal_resourcesblogspage ALTER COLUMN tip_2_number TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_resourcesblogspage ALTER COLUMN tip_2_number TYPE varchar(10);"
        ),
        migrations.RunSQL(
            "ALTER TABLE admin_portal_resourcesblogspage ALTER COLUMN tip_3_number TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_resourcesblogspage ALTER COLUMN tip_3_number TYPE varchar(10);"
        ),
        
        # SiteSettings fields
        migrations.RunSQL(
            "ALTER TABLE admin_portal_sitesettings ALTER COLUMN primary_color TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_sitesettings ALTER COLUMN primary_color TYPE varchar(7);"
        ),
        migrations.RunSQL(
            "ALTER TABLE admin_portal_sitesettings ALTER COLUMN secondary_color TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_sitesettings ALTER COLUMN secondary_color TYPE varchar(7);"
        ),
        migrations.RunSQL(
            "ALTER TABLE admin_portal_sitesettings ALTER COLUMN accent_color TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_sitesettings ALTER COLUMN accent_color TYPE varchar(7);"
        ),
        migrations.RunSQL(
            "ALTER TABLE admin_portal_sitesettings ALTER COLUMN google_analytics_id TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_sitesettings ALTER COLUMN google_analytics_id TYPE varchar(50);"
        ),
        migrations.RunSQL(
            "ALTER TABLE admin_portal_sitesettings ALTER COLUMN facebook_pixel_id TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_sitesettings ALTER COLUMN facebook_pixel_id TYPE varchar(50);"
        ),
        migrations.RunSQL(
            "ALTER TABLE admin_portal_sitesettings ALTER COLUMN privacy_policy_url TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_sitesettings ALTER COLUMN privacy_policy_url TYPE varchar(200);"
        ),
        migrations.RunSQL(
            "ALTER TABLE admin_portal_sitesettings ALTER COLUMN terms_of_service_url TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_sitesettings ALTER COLUMN terms_of_service_url TYPE varchar(200);"
        ),
        
        # Service pillar page content fields
        migrations.RunSQL(
            "ALTER TABLE admin_portal_strategicadvisorypagecontent ALTER COLUMN hero_image TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_strategicadvisorypagecontent ALTER COLUMN hero_image TYPE varchar(200);"
        ),
        migrations.RunSQL(
            "ALTER TABLE admin_portal_operationalsystemspagecontent ALTER COLUMN hero_image TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_operationalsystemspagecontent ALTER COLUMN hero_image TYPE varchar(200);"
        ),
        migrations.RunSQL(
            "ALTER TABLE admin_portal_livingsystemspagecontent ALTER COLUMN hero_image TYPE varchar(500);",
            reverse_sql="ALTER TABLE admin_portal_livingsystemspagecontent ALTER COLUMN hero_image TYPE varchar(200);"
        ),
    ]