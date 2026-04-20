import psycopg2

def sync_it():
    try:
        db_url = "postgres://app_user:Ojugbele2006#@34.134.52.218/my_production_db"
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        
        # 1. Page Content
        page_it = {
            "hero_title": "Come Operiamo",
            "meta_title": "Metodologia ORR Solutions - Come Operiamo",
            "meta_description": "Scopri il nostro metodo in 5 fasi per ottimizzare la tua organizzazione attraverso la consulenza strategica e i sistemi digitali."
        }
        
        for k, v in page_it.items():
            cur.execute(f"UPDATE admin_portal_howweoperatepagecontent SET {k}_it = jsonb_build_object('format', 'html', 'content', %s)", (v,))
            
        # 2. Process Steps
        steps_it = {
            1: {
                "title": "L'Inizio",
                "bullet1": "Una conversazione tranquilla.",
                "bullet2": "Un problema.",
                "bullet3": "Un punto di pressione.",
                "bullet4": "Una storia che finalmente viene raccontata.",
                "description1": "Ascoltiamo. In modo approfondito.",
                "description2": "Non per diagnosticare troppo in fretta, non per impressionare —",
                "description3": "ma per capire come respira effettivamente la tua organizzazione.",
                "description4": "Mentre scorri, lo schermo si illumina con il tuo mondo: i sistemi che hai costruito, i vuoti che tolleri, le idee che non hai ancora espresso."
            },
            2: {
                "title": "La Prima Mappa",
                "subtitle": "Dopo l'incontro, il rumore si placa.",
                "description": "Apriamo una pagina bianca e iniziamo a disegnare la prima mappa della tua organizzazione: dove le cose scorrono, dove si bloccano, dove l'energia nascosta si disperde.",
                "bullet1": "Nessun fronzolo.",
                "bullet2": "Nessuna offerta commerciale.",
                "bullet3": "Solo riflessioni scritte — il tuo fascicolo inizia qui.",
                "description1": "Questo diventa la colonna vertebrale di tutto ciò che segue."
            },
            3: {
                "title": "L'Approfondimento",
                "subtitle": "La mappa si affina.",
                "description": "Attingiamo alle giuste forme di intelligenza: intuizione del settore, ricerca mirata, scheletri normativi, modelli operativi, opportunità AI, ombre di rischio.",
                "bullet1": "Solo ciò che aggiunge valore.",
                "bullet2": "Nessuna offerta commerciale.",
                "bullet3": "Nulla che gonfi il processo.",
                "description1": "Il tuo mondo diventa più chiaro, non più grande."
            },
            4: {
                "title": "La Seconda Conversazione",
                "subtitle": "Ora le domande si fanno più affilate.",
                "bullet1": "Torniamo da te — brevemente, con precisione.",
                "bullet2": "Per testare i presupposti.",
                "bullet3": "Per correggere il tono.",
                "bullet4": "Per riallineare la mappa con la realtà che abiti.",
                "description1": "Qui il documento smette di essere un'analisi e inizia a diventare un progetto d'azione."
            },
            5: {
                "title": "Il Rapporto ORR",
                "subtitle": "Arrivi al punto della decisione.",
                "description": "Quello che ricevi non è una decorazione, ma un modello strutturato e pronto per la decisione:",
                "bullet1": "Cosa sta succedendo.",
                "bullet2": "Perché sta succedendo.",
                "bullet3": "Cosa deve cambiare ora.",
                "bullet4": "Cosa può crescere più avanti.",
                "bullet5": "E un modus operandi che lega tutto insieme.",
                "description1": "Un progetto che si regge da solo. Con noi o senza di noi."
            },
            6: {
                "title": "L'Architettura degli Incontri",
                "subtitle": "Dietro le quinte, il ritmo è semplice:",
                "description": "Primo Incontro → Scoperta → Follow-Up → Revisione del Rapporto",
                "bullet1": "Ognuno breve.",
                "bullet2": "Ognuno deliberato.",
                "bullet3": "Ognuno progettato per far avanzare il caso, mai lateralmente.",
                "description1": "Questa cadenza mantiene il processo leggero, mentre la riflessione rimane profonda."
            },
            7: {
                "title": "La Scelta",
                "subtitle": "Con il rapporto in mano, scegli il percorso:",
                "bullet1": "Fermati qui.",
                "bullet2": "Usa il progetto internamente.",
                "bullet3": "Continua.",
                "bullet4": "Lascia che ORR coordini l'implementazione,",
                "bullet5": "strutturi i tuoi sistemi,",
                "bullet6": "affini le tue operazioni,",
                "bullet7": "e supporti la tua crescita attraverso una relazione duratura.",
                "wordbreak": "OPPURE",
                "description1": "In ogni caso:",
                "description2": "te ne andrai con chiarezza."
            },
            8: {
                "title": "Il Portale",
                "subtitle": "Se rimani con noi, il lavoro cambia marcia.",
                "description": "Il Portale Client sblocca:",
                "bullet1": "i tuoi incontri,",
                "bullet2": "i tuoi documenti,",
                "bullet3": "i tuoi compiti,",
                "bullet4": "le tue intuizioni,",
                "bullet5": "il tuo Spazio di Lavoro.",
                "bullet8": "Un'unica interfaccia.",
                "bullet9": "Nessuna email sparsa.",
                "description2": "Un unico livello di coordinamento per la tua trasformazione continua."
            },
            9: {
                "title": "La Filosofia alla Base",
                "subtitle": "In ogni fase, il modello regge:",
                "description": "Scoprire → Diagnosticare → Progettare → Implementare → Crescere",
                "description1": "È il metodo del Business GP — il modo silenzioso e strutturato per stabilizzare un'organizzazione e poi aiutarla a operare come un sistema vivente:",
                "description2": "coerente, adattivo, reattivo."
            },
            10: {
                "title": "L'Invito",
                "subtitle": "Se questo approccio sembra diverso, è perché lo è.",
                "description1": "È più lento all'inizio, più veloce alla fine e più chiaro per tutto il percorso.",
                "description2": "Inizia con un incontro. Tutto il resto si svilupperà da lì.",
                "button_text": "Prenota il Tuo Primo Incontro",
                "button_text2": "Esplora i nostri servizi",
                "button_text3": "Accedi al Portale Client"
            }
        }
        
        print("Syncing Process Steps (Italian)...")
        for step_id, fields in steps_it.items():
            for k, v in fields.items():
                cur.execute(f"UPDATE admin_portal_processstep SET {k}_it = jsonb_build_object('format', 'html', 'content', %s) WHERE id = %s", (v, step_id))
        
        conn.commit()
        conn.close()
        print("ITALIAN SYNC COMPLETE.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    sync_it()
