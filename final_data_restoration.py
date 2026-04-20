import psycopg2

def final_restore():
    try:
        db_url = "postgres://app_user:Ojugbele2006#@34.134.52.218/my_production_db"
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        
        # List of tables to restore
        tables = {
            'admin_portal_homepage': ['hero_title', 'hero_subtitle', 'hero_cta_text', 'about_title', 'about_content', 'services_title', 'services_subtitle', 'contact_title', 'contact_subtitle'],
            'admin_portal_servicestage': ['title', 'subtitle', 'description', 'focus_content', 'button_text'],
            'admin_portal_servicepillar': ['title', 'description', 'button_text'],
            'admin_portal_servicespagecontent': ['hero_title', 'hero_subtitle', 'pillars_title', 'business_gp_title', 'business_gp_subtitle', 'business_gp_description', 'business_gp_button_text'],
            'admin_portal_approachsection': ['title', 'paragraph_1', 'paragraph_2', 'paragraph_3'],
            'admin_portal_orrrolesection': ['title', 'description'],
            'admin_portal_messagestrip': ['title', 'message'],
            'admin_portal_orrreportsection': ['title', 'description'],
            'admin_portal_faq': ['question', 'answer']
        }

        print("Restoring all English content (Final Forced Sync)...")
        for table, fields in tables.items():
            print(f"Table: {table}")
            for field in fields:
                en_field = f"{field}_en"
                
                # Check column info
                cur.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name='{table}' AND column_name IN ('{field}', '{en_field}')")
                cols = {r[0]: r[1] for r in cur.fetchall()}
                
                if field not in cols or en_field not in cols:
                    continue
                
                # Logic to handle JSONB vs Plain Text
                if cols[en_field] == 'jsonb' and cols[field] != 'jsonb':
                    # Wrap plain text into JSONB structure
                    sync_sql = f"{en_field} = jsonb_build_object('format', 'html', 'content', {field})"
                else:
                    # Direct cast
                    sync_sql = f"{en_field} = {field}::jsonb"

                query = f"UPDATE {table} SET {sync_sql} WHERE {field} IS NOT NULL AND {field} != ''"
                cur.execute(query)
                if cur.rowcount > 0:
                    print(f"  - {en_field}: {cur.rowcount} rows restored.")
        
        conn.commit()
        conn.close()
        print("\nSUCCESS: All English content is now synchronized and visible.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    final_restore()
