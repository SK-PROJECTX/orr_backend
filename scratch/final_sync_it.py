import os
import psycopg2
import json

db_pass = os.environ.get('DB_PASS')

def to_jsonb_str(content):
    return json.dumps({"content": content, "format": "html"})

updates = [
    # HomePage
    (
        "admin_portal_homepage",
        {
            "hero_title_it": "Trasforma il tuo Business con ORR",
            "hero_subtitle_it": "Consulenza Strategica, Innovazione Digitale e Soluzioni di Crescita Sostenibile",
            "hero_cta_text_it": "Inizia Ora",
            "about_title_it": "Chi è ORR",
            "about_content_it": "Aiutiamo le organizzazioni a navigare sfide complesse, ottimizzare le operazioni e sbloccare il loro pieno potenziale attraverso una consulenza esperta e soluzioni digitali su misura.",
            "services_title_it": "I Nostri Servizi"
        },
        1
    ),
    # ApproachSection (The Supporting Copy requested)
    (
        "admin_portal_approachsection",
        {
            "title_it": "L'Approccio ORR",
            "paragraph_1_it": "Proprio come un medico di base esperto, partiamo dalla vostra storia, non dal nostro framework. Ci prendiamo il tempo per capire come funziona davvero la vostra azienda prima di prescrivere qualsiasi cosa.",
            "paragraph_2_it": "Non siamo un consulente solitario — siamo un livello di coordinamento centrale con una rete distribuita alle spalle. Quando necessario, attingiamo a specialisti in tutti i continenti, ma avrete sempre un unico punto di contatto: ORR, focalizzato su ciò che è meglio per voi.",
            "paragraph_3_it": "Sistemiamo ciò che vi rallenta, rafforziamo i sistemi in base a come lavorano effettivamente le vostre persone e, quando è necessario un contributo più approfondito, lo introduciamo al momento giusto — sempre al servizio dei vostri obiettivi."
        },
        1
    ),
    # BusinessSystemSection
    (
        "admin_portal_businesssystemsection",
        {
            "title_it": "L'Azienda come Sistema Vivente",
            "subtitle_it": "Proprio come un corpo umano, le aziende moderne prosperano grazie alla connessione e al coordinamento.",
            "card_1_title_it": "Sistema Nervoso (Dati e Approfondimenti)",
            "card_1_description_it": "Un sistema di dati intelligente per informare le decisioni strategiche.",
            "card_2_title_it": "Sistema Circolatorio (Operazioni e Portata)",
            "card_2_description_it": "Operazioni fluide che supportano la crescita e l'efficienza.",
            "card_3_title_it": "Sistema Immunitario (Resilienza e Scalabilità)",
            "card_3_description_it": "Sistemi scalabili che proteggono e rafforzano la vostra azienda."
        },
        1
    )
]

def run_sync():
    conn = psycopg2.connect(
        dbname='my_production_db',
        user='postgres',
        password=db_pass,
        host='34.134.52.218',
        port='5432',
        sslmode='require'
    )
    conn.autocommit = True
    cursor = conn.cursor()
    
    print("Starting translation sync...")
    
    for table, fields, row_id in updates:
        print(f"Updating {table}...")
        set_clauses = []
        params = []
        for col, content in fields.items():
            set_clauses.append(f"{col} = %s")
            params.append(to_jsonb_str(content))
        
        # Also ensure the _en columns are populated if they are empty
        # (This avoids the empty strings I saw earlier)
        # However, for simplicity now I'll just focus on finishing the _it fields
        
        query = f"UPDATE {table} SET {', '.join(set_clauses)} WHERE id = %s"
        params.append(row_id)
        cursor.execute(query, params)
        print(f"[OK] {table} updated.")

    print("\nSync finished successfully!")
    conn.close()

if __name__ == "__main__":
    run_sync()
