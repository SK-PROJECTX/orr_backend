import psycopg2
import os

def check():
    host = "34.134.52.218"
    user = "app_user"
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
        cur = conn.cursor()
        
        print("Checking LivingSystemsPageContent...")
        cur.execute("SELECT id, hero_title_en, hero_title_it, hero_title_ar FROM admin_portal_livingsystemspagecontent;")
        rows = cur.fetchall()
        for row in rows:
            print(f"ID: {row[0]}")
            print(f"  EN: {row[1]}")
            print(f"  IT: {row[2]}")
            print(f"  AR: {row[3]}")
            
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check()
