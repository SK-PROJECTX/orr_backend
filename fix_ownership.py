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
        
        print("Connected! Granting roles...")
        
        try:
            # Become a member of app_user so we can reassign to it
            cur.execute("GRANT app_user TO postgres;")
            print("GRANT app_user TO postgres successful!")
        except Exception as e:
            print(f"FAILED GRANT ROLE: {e}")

        print("Reassigning owned objects...")
        try:
            cur.execute("REASSIGN OWNED BY postgres TO app_user;")
            print("REASSIGN OWNED BY postgres TO app_user successful!")
        except Exception as e:
            print(f"FAILED REASSIGN: {e}")

        try:
            cur.execute("GRANT ALL PRIVILEGES ON SCHEMA public TO app_user;")
            cur.execute("GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO app_user;")
            cur.execute("GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO app_user;")
            print("Grants successful!")
        except Exception as e:
            print(f"FAILED GRANTS: {e}")
            
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fix()
