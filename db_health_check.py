import psycopg2
import time

def health_check():
    db_url = "postgres://app_user:Ojugbele2006#@34.134.52.218/my_production_db"
    try:
        print("Attempting to connect with 60s timeout...")
        conn = psycopg2.connect(db_url, connect_timeout=60)
        cur = conn.cursor()
        cur.execute("SELECT version();")
        print(f"Connected! {cur.fetchone()}")
        conn.close()
    except Exception as e:
        print(f"Health Check Failed: {e}")

if __name__ == "__main__":
    health_check()
