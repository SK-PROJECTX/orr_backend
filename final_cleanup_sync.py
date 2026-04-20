import psycopg2

def final_sync():
    try:
        db_url = "postgres://app_user:Ojugbele2006#@34.134.52.218/my_production_db"
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        
        tables = {
            'admin_portal_processsection': ['title', 'subtitle', 'stage_1_title', 'stage_1_description', 'stage_2_title', 'stage_2_description', 'stage_3_title', 'stage_3_description', 'stage_4_title', 'stage_4_description', 'stage_5_title', 'stage_5_description'],
            'admin_portal_testimonial': ['text', 'author', 'role'],
            'admin_portal_businesssystemsection': ['title', 'subtitle', 'description'],
            'admin_portal_businesssystemcard': ['title', 'description', 'button_text'],
            'admin_portal_processstage': ['title', 'description'],
        }

        print("Executing Final Cleanup Restorative Sync...")
        for table, fields in tables.items():
            print(f"Table: {table}")
            for field in fields:
                en_field = f"{field}_en"
                
                # Check column existence
                cur.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name='{table}' AND column_name='{en_field}'")
                if not cur.fetchone():
                    continue

                query = f"""
                UPDATE {table} 
                SET {en_field} = jsonb_build_object('format', 'html', 'content', {field})
                WHERE {field} IS NOT NULL AND {field} != ''
                """
                cur.execute(query)
                if cur.rowcount > 0:
                    print(f"  [OK] {en_field}: {cur.rowcount} rows restored.")
        
        conn.commit()
        conn.close()
        print("\nALL CMS DATA RESTORATION PROCEDURES ARE NOW COMPLETE.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    final_sync()
