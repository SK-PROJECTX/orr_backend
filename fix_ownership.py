import psycopg2
import os

def fix():
    host = "34.134.52.218"
    user = "postgres"
    password = "Ojugbele2006#"
    dbname = "my_production_db"
    
    try:
        conn = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            dbname=dbname,
            sslmode="require"
        )
        conn.autocommit = True
        cur = conn.cursor()
        
        print("Connected! Fixing ownership...")
        
        # Grant ownership of all tables in public schema to app_user
        cur.execute("GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO app_user;")
        cur.execute("GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO app_user;")
        cur.execute("ALTER TABLE IF EXISTS admin_portal_approachsection OWNER TO app_user;")
        cur.execute("ALTER TABLE IF EXISTS admin_portal_homepage OWNER TO app_user;")
        cur.execute("ALTER TABLE IF EXISTS admin_portal_operationalsystemspagecontent OWNER TO app_user;")
        cur.execute("ALTER TABLE IF EXISTS admin_portal_strategicadvisorypagecontent OWNER TO app_user;")
        cur.execute("ALTER TABLE IF EXISTS admin_portal_livingsystemspagecontent OWNER TO app_user;")
        
        print("Ownership fixed!")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fix()
