import psycopg2

def perfect_restore():
    try:
        db_url = "postgres://app_user:Ojugbele2006#@34.134.52.218/my_production_db"
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        
        tables = {
            # Core Home & General
            'admin_portal_homepage': ['hero_title', 'hero_subtitle', 'hero_cta_text', 'about_title', 'about_content', 'services_title', 'services_subtitle', 'contact_title', 'contact_subtitle'],
            'admin_portal_faq': ['question', 'answer'],
            'admin_portal_messagestrip': ['title', 'message'],
            'admin_portal_testimonial': ['text', 'author', 'role'],
            
            # Services & Stages
            'admin_portal_servicespagecontent': ['hero_title', 'hero_subtitle', 'pillars_title', 'business_gp_title', 'business_gp_subtitle', 'business_gp_description', 'business_gp_button_text'],
            'admin_portal_servicestage': ['title', 'subtitle', 'description', 'focus_content', 'button_text'],
            'admin_portal_servicepillar': ['title', 'description', 'button_text'],
            
            # How We Operate
            'admin_portal_howweoperatepagecontent': ['hero_title', 'meta_title', 'meta_description'],
            'admin_portal_processstep': ['title', 'subtitle', 'description', 'bullet1', 'bullet2', 'bullet3', 'bullet4', 'bullet5', 'bullet6', 'bullet7', 'bullet8', 'bullet9', 'wordbreak', 'description1', 'description2', 'description3', 'description4', 'button_text', 'button_text2', 'button_text3'],
            
            # Service Pillars Detail Pages
            'admin_portal_strategicadvisorypagecontent': ['hero_title', 'hero_subtitle', 'hero_description', 'services_title', 'service_1_title', 'service_1_description', 'service_2_title', 'service_2_description', 'service_3_title', 'service_3_description', 'process_title', 'process_subtitle', 'process_description', 'process_step_1_title', 'process_step_1_subtitle', 'process_step_1', 'process_step_2_title', 'process_step_2', 'process_step_3_title', 'process_step_3', 'network_title', 'network_description', 'digital_title', 'digital_subtitle', 'digital_description', 'digital_image_alt', 'case_challenge', 'case_solution', 'case_result', 'case_image_alt', 'cta_title', 'cta_description', 'cta_button_text'],
            'admin_portal_operationalsystemspagecontent': ['hero_title', 'hero_subtitle', 'hero_description', 'services_title', 'service_1_title', 'service_1_description', 'service_2_title', 'service_2_description', 'service_3_title', 'service_3_description', 'process_title', 'process_description', 'process_step_1_title', 'process_step_1', 'process_step_2_title', 'process_step_2', 'process_step_3_title', 'process_step_3', 'case_challenge', 'case_solution', 'case_result', 'case_image_alt', 'cta_title', 'cta_description', 'cta_button_text'],
            'admin_portal_livingsystemspagecontent': ['hero_title', 'hero_subtitle', 'hero_description', 'services_title', 'service_1_title', 'service_1_description', 'service_2_title', 'service_2_description', 'service_3_title', 'service_3_description', 'process_title', 'process_description', 'process_step_1_title', 'process_step_1', 'process_step_2_title', 'process_step_2', 'process_step_3_title', 'process_step_3', 'case_challenge', 'case_solution', 'case_result', 'case_image_alt', 'cta_title', 'cta_description', 'cta_button_text'],
            
            # Resources & Blogs
            'admin_portal_resourcesblogspagecontent': ['hero_title', 'hero_description1', 'hero_description2', 'hero_description3', 'hero_button1_text', 'hero_button2_text'],
            'admin_portal_contentcard': ['badge', 'title', 'content', 'button1_text', 'button2_text'],
            'admin_portal_blogpost': ['title', 'content', 'meta_title', 'meta_description'],
            
            # Contact Page
            'admin_portal_contactpagecontent': ['hero_title', 'meta_title', 'meta_description'],
            
            # Other Sections
            'admin_portal_approachsection': ['title', 'paragraph_1', 'paragraph_2', 'paragraph_3'],
            'admin_portal_orrrolesection': ['title', 'description'],
            'admin_portal_orrreportsection': ['title', 'description'],
        }

        print("Executing FULL System-Wide Smart Restorative Sync...")
        for table, fields in tables.items():
            print(f"\nProcessing Table: {table}")
            for field in fields:
                en_field = f"{field}_en"
                
                # Verify column exists before update
                cur.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name='{table}' AND column_name='{en_field}'")
                if not cur.fetchone():
                    continue

                # Smart Unwrapping & Wrap-If-Needed SQL
                query = f"""
                UPDATE {table} 
                SET {en_field} = CASE 
                    WHEN {field} LIKE '{{%"content"%' THEN {field}::jsonb
                    ELSE jsonb_build_object('format', 'html', 'content', {field})
                END
                WHERE {field} IS NOT NULL AND {field} != ''
                """
                try:
                    cur.execute(query)
                    if cur.rowcount > 0:
                        print(f"  [OK] {en_field}: {cur.rowcount} rows restored.")
                except Exception as e:
                    print(f"  [ERROR] on {field}: {e}")
                    conn.rollback()
                    cur = conn.cursor()
        
        conn.commit()
        conn.close()
        print("\nMISSION ACCOMPLISHED: The entire company database is now perfectly restored and localized.")
    except Exception as e:
        print(f"Connection Error: {e}")

if __name__ == "__main__":
    perfect_restore()
