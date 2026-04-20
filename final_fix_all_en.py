import psycopg2

def final_fix():
    try:
        db_url = "postgres://app_user:Ojugbele2006#@34.134.52.218/my_production_db"
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        
        # This list covers the structures where we KNOW table names and fields
        # (Table, Fields, IsPlainText)
        sync_plans = [
            ('admin_portal_homepage', ['hero_title', 'hero_subtitle', 'hero_cta_text', 'about_title', 'about_content', 'services_title', 'services_subtitle', 'contact_title', 'contact_subtitle', 'meta_title', 'meta_description'], False),
            ('admin_portal_servicestage', ['title', 'subtitle', 'description', 'focus_content', 'button_text'], False),
            ('admin_portal_servicepillar', ['title', 'description', 'button_text'], False),
            ('admin_portal_servicespagecontent', ['hero_title', 'hero_subtitle', 'pillars_title', 'business_gp_title', 'business_gp_subtitle', 'business_gp_description', 'business_gp_button_text', 'meta_title', 'meta_description'], False),
            ('admin_portal_approachsection', ['title', 'paragraph_1', 'paragraph_2', 'paragraph_3'], False),
            ('admin_portal_businesssystemsection', ['title', 'subtitle', 'card_1_title', 'card_1_description', 'card_2_title', 'card_2_description', 'card_3_title', 'card_3_description'], False),
            ('admin_portal_processsection', ['title', 'subtitle', 'stage_1_title', 'stage_1_description', 'stage_2_title', 'stage_2_description', 'stage_3_title', 'stage_3_description', 'stage_4_title', 'stage_4_description'], False),
            ('admin_portal_faq', ['question', 'answer'], True),
            ('admin_portal_orrrolesection', ['title', 'description'], True),
            ('admin_portal_messagestrip', ['title', 'message'], True),
            ('admin_portal_orrreportsection', ['title', 'description'], True)
        ]
        
        print("Finalizing Global English Data Restoration...")
        
        for table, fields, is_plain_text in sync_plans:
            print(f"Table: {table}")
            for field in fields:
                en_field = f"{field}_en"
                
                # Check column info
                cur.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name='{table}' AND column_name IN ('{field}', '{en_field}')")
                cols = {r[0]: r[1] for r in cur.fetchall()}
                
                if field not in cols or en_field not in cols:
                    continue

                if is_plain_text:
                    sync_sql = f"{en_field} = jsonb_build_object('format', 'html', 'content', {field})"
                else:
                    sync_sql = f"{en_field} = {field}::jsonb"

                # Update EVERYTHING that has data in the base column
                # This is the "Force" part. 
                query = f"UPDATE {table} SET {sync_sql} WHERE {field} IS NOT NULL AND {field} != ''"
                
                try:
                    cur.execute(query)
                    if cur.rowcount > 0:
                        print(f"  - Synchronized {field} -> {en_field} ({cur.rowcount} rows)")
                except Exception as e:
                    print(f"  - Error in {field}: {e}")
                    conn.rollback()
                    cur = conn.cursor()
        
        conn.commit()
        print("\nCOMPLETED: All English content is now fully synchronized and visible.")
        conn.close()
    except Exception as e:
        print(f"Fatal Error: {e}")

if __name__ == "__main__":
    final_fix()
