import os
import psycopg2

db_pass = os.environ.get('DB_PASS')

conn = psycopg2.connect(
    dbname="my_production_db",
    user="postgres",
    password=db_pass,
    host="34.134.52.218",
    port="5432",
    sslmode="require"
)
conn.autocommit = True
cursor = conn.cursor()

try:
    for table in ['admin_portal_homepage', 'admin_portal_approachsection', 'admin_portal_businesssystemsection']:
        print(f"Checking table {table}...")
        cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name='{table}' AND (column_name LIKE '%_en' OR column_name LIKE '%_it')")
        columns = [row[0] for row in cursor.fetchall()]
        for col in columns:
            print(f'Dropping {col} from {table}...')
            cursor.execute(f'ALTER TABLE {table} DROP COLUMN IF EXISTS {col} CASCADE;')
    print("Cleanup finished!")
finally:
    cursor.close()
    conn.close()
