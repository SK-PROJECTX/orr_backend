import psycopg2

def repair_content():
    try:
        db_url = "postgres://app_user:Ojugbele2006#@34.134.52.218/my_production_db"
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        
        content_map = [
            ('admin_portal_homepage', [
                'hero_title', 'hero_subtitle', 'hero_cta_text', 
                'about_title', 'about_content', 
                'services_title', 'services_subtitle',
                'contact_title', 'contact_subtitle',
                'meta_title', 'meta_description'
            ]),
            ('admin_portal_servicestage', ['title', 'subtitle', 'description', 'focus_content', 'button_text']),
            ('admin_portal_servicepillar', ['title', 'description', 'button_text']),
            ('admin_portal_servicespagecontent', [
                'hero_title', 'hero_subtitle', 'pillars_title', 
                'business_gp_title', 'business_gp_subtitle', 'business_gp_description', 'business_gp_button_text',
                'meta_title', 'meta_description'
            ]),
            ('admin_portal_approachsection', ['title', 'paragraph_1', 'paragraph_2', 'paragraph_3']),
            ('admin_portal_businesssystemsection', [
                'title', 'subtitle', 
                'card_1_title', 'card_1_description',
                'card_2_title', 'card_2_description',
                'card_3_title', 'card_3_description'
            ]),
            ('admin_portal_processsection', [
                'title', 'subtitle',
                'stage_1_title', 'stage_1_description',
                'stage_2_title', 'stage_2_description',
                'stage_3_title', 'stage_3_description',
                'stage_4_title', 'stage_4_description'
            ]),
            ('admin_portal_orrrolesection', ['title', 'description'], True),
            ('admin_portal_messagestrip', ['title', 'message']),
            ('admin_portal_orrreportsection', ['title', 'description']),
            ('admin_portal_testimonial', ['author_name', 'author_title', 'content']),
            ('admin_portal_faq', ['question', 'answer'], True),
            ('admin_portal_blogpost', ['title', 'summary', 'content', 'meta_title', 'meta_description']),
            ('admin_portal_contactinfo', ['address', 'email', 'phone', 'working_hours'])
        ]
        
        print("Restoring English localization content (Phase 3 - Forced Sync)...")
        
        for item in content_map:
            table = item[0]
            fields = item[1]
            wrap_json = item[2] if len(item) > 2 else False
            
            print(f"\nProcessing table: {table}")
            for field in fields:
                en_field = f"{field}_en"
                
                # Check column info
                cur.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name='{table}' AND column_name IN ('{field}', '{en_field}')")
                cols = {r[0]: r[1] for r in cur.fetchall()}
                
                if field not in cols or en_field not in cols:
                    continue

                # Prepare SET clause
                if wrap_json:
                    set_clause = f"{en_field} = jsonb_build_object('format', 'html', 'content', {field})"
                elif cols[en_field] == 'jsonb':
                    set_clause = f"{en_field} = {field}::jsonb"
                else:
                    set_clause = f"{en_field} = {field}"

                # Aggressive Update query: Sync if English is NULL, empty string, null JSON, or has empty content
                # We use multiple conditions to catch all variants of 'empty'
                query = f"""
                UPDATE {table}
                SET {set_clause}
                WHERE 
                    {field} IS NOT NULL AND (
                        {en_field} IS NULL OR 
                        {en_field}::text = '""' OR 
                        {en_field}::text = 'null' OR 
                        {en_field}::text = '{{}}' OR
                        ({en_field}::text LIKE '%"content": ""%') OR
                        ({en_field}::text LIKE '%"content": null%')
                    );
                """
                try:
                    cur.execute(query)
                    if cur.rowcount > 0:
                        print(f"  - Synced field: {field} -> {en_field} ({cur.rowcount} rows)")
                except Exception as e:
                    print(f"  - Error syncing {field}: {e}")
                    conn.rollback()
        
        conn.commit()
        print("\nSUCCESS: English fallback content restored.")
        conn.close()
    except Exception as e:
        print(f"Fatal Error: {e}")

if __name__ == "__main__":
    repair_content()
