import psycopg2

def recover_steps():
    try:
        db_url = "postgres://app_user:Ojugbele2006#@34.134.52.218/my_production_db"
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        
        # We target all steps (1-10) and all their fields
        table = 'admin_portal_processstep'
        fields = ['title', 'subtitle', 'description', 'bullet1', 'bullet2', 'bullet3', 'bullet4', 'bullet5', 'bullet6', 'bullet7', 'bullet8', 'bullet9', 'wordbreak', 'description1', 'description2', 'description3', 'description4', 'button_text', 'button_text2', 'button_text3']

        print(f"Starting Dedicated Recovery for {table}...")
        for field in fields:
            en_field = f"{field}_en"
            
            # For these, we will FORCE the wrap because we saw they were plain text in the DB
            query = f"""
            UPDATE {table} 
            SET {en_field} = jsonb_build_object('format', 'html', 'content', {field})
            WHERE {field} IS NOT NULL AND {field} != ''
            """
            try:
                cur.execute(query)
                if cur.rowcount > 0:
                    print(f"  [FIXED] {en_field}: {cur.rowcount} rows restored.")
            except Exception as e:
                print(f"  [ERROR] {en_field}: {e}")
                conn.rollback()
                cur = conn.cursor()
        
        # Also fix the How We Operate Page Content header
        header_table = 'admin_portal_howweoperatepagecontent'
        header_fields = ['hero_title', 'meta_title', 'meta_description']
        print(f"Starting Dedicated Recovery for {header_table}...")
        for field in header_fields:
            en_field = f"{field}_en"
            query = f"""
            UPDATE {header_table} 
            SET {en_field} = jsonb_build_object('format', 'html', 'content', {field})
            WHERE {field} IS NOT NULL AND {field} != ''
            """
            cur.execute(query)
            if cur.rowcount > 0:
                print(f"  [FIXED] {en_field}: {cur.rowcount} rows restored.")

        conn.commit()
        conn.close()
        print("\nHOW WE OPERATE RECOVERY COMPLETE.")
    except Exception as e:
        print(f"Connection Error: {e}")

if __name__ == "__main__":
    recover_steps()
