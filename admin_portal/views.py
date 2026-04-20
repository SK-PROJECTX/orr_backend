from django.shortcuts import render
from django.http import JsonResponse
from admin_portal.models import (
    HowWeOperatePageContent, ProcessStep, 
    ServicesPageContent, ServiceStage, ServicePillar,
    Testimonial, MessageStrip
)

def sync_cms_it_view(request):
    """
    Consolidated view to trigger Italian translation sync for all CMS pages.
    Visit: /admin-portal/sync-it-translations-secret/
    """
    try:
        # --- 1. HOW WE OPERATE PAGE ---
        page_it = {
            "hero_title": "Come Operiamo",
            "meta_title": "Metodologia ORR Solutions - Come Operiamo",
            "meta_description": "Scopri il nostro metodo in 5 fasi per ottimizzare la tua organizzazione attraverso la consulenza strategica e i sistemi digitali."
        }
        how_page = HowWeOperatePageContent.objects.first()
        if how_page:
            for k, v in page_it.items():
                setattr(how_page, f"{k}_it", {"format": "html", "content": v})
            how_page.save()

        # --- 2. HOW WE OPERATE STEPS (1-10) ---
        steps_it = {
            1: {"title": "L'Inizio", "bullet1": "Una conversazione tranquilla.", "bullet2": "Un problema.", "bullet3": "Un punto di pressione.", "bullet4": "Una storia che finalmente viene raccontata.", "description1": "Ascoltiamo. In modo approfondito.", "description2": "Non per diagnosticare troppo in fretta, non per impressionare —", "description3": "ma per capire come respira effettivamente la tua organizzazione.", "description4": "Mentre scorri, lo schermo si illumina con il tuo mondo: i sistemi che hai costruito, i vuoti che tolleri, le idee che non hai ancora espresso."},
            2: {"title": "La Prima Mappa", "subtitle": "Dopo l'incontro, il rumore si placa.", "description": "Apriamo una pagina bianca e iniziamo a disegnare la prima mappa della tua organizzazione: dove le cose scorrono, dove si bloccano, dove l'energia nascosta si disperde.", "bullet1": "Nessun fronzolo.", "bullet2": "Nessuna offerta commerciale.", "bullet3": "Solo riflessioni scritte — il tuo fascicolo inizia qui.", "description1": "Questo diventa la colonna vertebrale di tutto ciò che segue."},
            3: {"title": "L'Approfondimento", "subtitle": "La mappa si affina.", "description": "Attingiamo alle giuste forme di intelligenza: intuizione del settore, ricerca mirata, scheletri normativi, modelli operativi, opportunità AI, ombre di rischio.", "bullet1": "Solo ciò che aggiunge valore.", "bullet2": "Nessuna offerta commerciale.", "bullet3": "Nulla che gonfi il processo.", "description1": "Il tuo mondo diventa più chiaro, non più grande."},
            4: {"title": "La Seconda Conversazione", "subtitle": "Ora le domande si fanno più affilate.", "bullet1": "Torniamo da te — brevemente, con precisione.", "bullet2": "Per testare i presupposti.", "bullet3": "Per correggere il tono.", "bullet4": "Per riallineare la mappa con la realtà che abiti.", "description1": "Qui il documento smette di essere un'analisi e inizia a diventare un progetto d'azione."},
            5: {"title": "Il Rapporto ORR", "subtitle": "Arrivi al punto della decisione.", "description": "Quello che ricevi non è una decorazione, ma un modello strutturato e pronto per la decisione:", "bullet1": "Cosa sta succedendo.", "bullet2": "Perché sta succedendo.", "bullet3": "Cosa deve cambiare ora.", "bullet4": "Cosa può crescere più avanti.", "bullet5": "E un modus operandi che lega tutto insieme.", "description1": "Un progetto che si regge da solo. Con noi o senza di noi."},
            6: {"title": "L'Architettura degli Incontri", "subtitle": "Dietro le quinte, il ritmo è semplice:", "description": "Primo Incontro → Scoperta → Follow-Up → Revisione del Rapporto", "bullet1": "Ognuno breve.", "bullet2": "Ognuno deliberato.", "bullet3": "Ognuno progettato per far avanzare il caso, mai lateralmente.", "description1": "Questa cadenza mantiene il processo leggero, mentre la riflessione rimane profonda."},
            7: {"title": "La Scelta", "subtitle": "Con il rapporto in mano, scegli il percorso:", "bullet1": "Fermati qui.", "bullet2": "Usa il progetto internamente.", "bullet3": "Continua.", "bullet4": "Lascia che ORR coordini l'implementazione,", "bullet5": "strutturi i tuoi sistemi,", "bullet6": "affini le tue operazioni,", "bullet7": "e supporti la tua crescita attraverso una relazione duratura.", "wordbreak": "OPPURE", "description1": "In ogni caso:", "description2": "te ne andrai con chiarezza."},
            8: {"title": "Il Portale", "subtitle": "Se rimani con noi, il lavoro cambia marcia.", "description": "Il Portale Client sblocca:", "bullet1": "i tuoi incontri,", "bullet2": "i tuoi documenti,", "bullet3": "i tuoi compiti,", "bullet4": "le tue intuizioni,", "bullet5": "il tuo Spazio di Lavoro.", "bullet8": "Un'unica interfaccia.", "bullet9": "Nessuna email sparsa.", "description2": "Un unico livello di coordinamento per la tua trasformazione continua."},
            9: {"title": "La Filosofia alla Base", "subtitle": "In ogni fase, il modello regge:", "description": "Scoprire → Diagnosticare → Progettare → Implementare → Crescere", "description1": "È il metodo del Business GP — il modo silenzioso e strutturato per stabilizzare un'organizzazione e poi aiutarla a operare come un sistema vivente:", "description2": "coerente, adattivo, reattivo."},
            10: {"title": "L'Invito", "subtitle": "Se questo approccio sembra diverso, è perché lo è.", "description1": "È più lento all'inizio, più veloce alla fine e più chiaro per tutto il percorso.", "description2": "Inizia con un incontro. Tutto il resto si svilupperà da lì.", "button_text": "Prenota il Tuo Primo Incontro", "button_text2": "Esplora i nostri servizi", "button_text3": "Accedi al Portale Client"}
        }
        for s_id, f in steps_it.items():
            s = ProcessStep.objects.filter(id=s_id).first()
            if s:
                for k, v in f.items(): setattr(s, f"{k}_it", {"format": "html", "content": v})
                s.save()

        # --- 3. SERVICES PAGE CONTENT ---
        svc_page_it = {
            "hero_title": "ORR Solutions - Ascolta. Risolvi. Ottimizza.",
            "hero_subtitle": "Trattiamo la tua organizzazione come un intero sistema: digitale, normativo e vivente. Ascoltiamo prima di tutto, poi progettiamo il giusto mix di consulenza, sistemi, AI e progetti sul campo in modo che tu possa muoverti meglio e crescere in modo più intelligente.",
            "pillars_title": "I Tre Pilastri",
            "business_gp_title": "ORR è il tuo Business GP per",
            "business_gp_subtitle": "sistemi complessi: digitali e viventi.",
            "business_gp_description": "Ascoltiamo l'intera organizzazione, risolviamo con struttura e visione, e ottimizziamo affinché tu possa crescere con fiducia.",
            "business_gp_button_text": "Contattaci"
        }
        svc_page = ServicesPageContent.objects.first()
        if svc_page:
            for k, v in svc_page_it.items():
                setattr(svc_page, f"{k}_it", {"format": "html", "content": v})
            svc_page.save()

        # --- 4. SERVICE STAGES (1-5) ---
        svc_stages_it = {
            1: {
                "title": "FASE 1 - SCOPERTA", 
                "subtitle": "Ascolta.", 
                "description": "Iniziamo in modo semplice: una conversazione tranquilla e una scansione rapida della tua realtà.",
                "focus_content": "Ci concentriamo su:\n• Il tuo contesto, le persone e le pressioni\n• Rischi normativi, operativi, dei dati e ambientali\n• Quali domande contano davvero",
                "button_text": "Iscriviti"
            },
            2: {
                "title": "FASE 2 - DIAGNOSI", 
                "subtitle": "Pensa. Poi ascolta di nuovo.", 
                "description": "Trasformiamo i sintomi in una mappa chiara di problemi e opportunità attraverso i tre pilastri.",
                "focus_content": "Cosa succede qui:\n• Mappatura dei colli di bottiglia e dei processi\n• Revisione di conformità, governance e rischio\n• Scansione dei dati e dei sistemi viventi\n• Elenco prioritario: urgente, alto impatto, più avanti",
                "button_text": "Scopri di Più"
            },
            3: {
                "title": "FASE 3 - PROGETTAZIONE", 
                "subtitle": "Progetta.", 
                "description": "Progettiamo strutture pratiche, non presentazioni teoriche.",
                "focus_content": "Output Tipici:\n• SOP e flussi di lavoro standardizzati\n• Percorsi di comunicazione e decisione\n• Stack tecnologico, integrazione e casi d'uso AI\n• Concetti semplici per progetti sul campo o di sviluppo\n• Dati puliti e strutturati pronti per la reportistica",
                "button_text": "Iscriviti"
            },
            4: {
                "title": "FASE 4 - IMPLEMENTAZIONE", 
                "subtitle": "Risolvi nella pratica.", 
                "description": "Il progetto diventa realtà con un'implementazione guidata.",
                "focus_content": "L'implementazione può includere:\n• Configurazione amministrativa e dei record\n• Registrazione clienti, pipeline e flussi di follow-up\n• Dashboard KPI con riepiloghi AI\n• Formazione del personale negli strumenti già in uso\n• Collegamento con fornitori esterni dove necessario",
                "button_text": "Contattaci"
            },
            5: {
                "title": "FASE 5 - CRESCITA", 
                "subtitle": "Ottimizza.", 
                "description": "Una volta che i sistemi sono attivi, continuiamo a farli imparare.",
                "focus_content": "Come supportiamo la crescita:\n• Acquisizione continua di dati e analisi leggera\n• Revisioni trimestrali e messa a punto del sistema\n• Monitoraggio assistito dall'AI e avvisi precoci\n• Scenari e pensiero 'cosa succederebbe se'\n• Check-in regolari e leggeri: la clinica dei tuoi sistemi",
                "button_text": "Iscriviti"
            }
        }
        for st_num, f in svc_stages_it.items():
            st = ServiceStage.objects.filter(stage_number=st_num).first()
            if st:
                for k, v in f.items(): setattr(st, f"{k}_it", {"format": "html", "content": v})
                st.save()

        # --- 5. SERVICE PILLARS ---
        svc_pillars_it = {
            1: {"title": "Consulenza Strategica e Conformità", "description": "Chiarezza breve e incisiva su regole, rischi e direzione — dalla normativa ed ESG alle questioni biotecnologiche e ambientali.", "button_text": "Scopri di più"},
            2: {"title": "Sistemi Digitali, Automazione e AI", "description": "SOP, flussi di lavoro, portali, dashboard e assistenti AI che rendono il lavoro fluido con meno sforzo e meno sorprese.", "button_text": "Scopri di più"},
            3: {"title": "Sistemi Viventi e Rigenerazioni", "description": "Supporto per terra, acqua, specie ed ecosistemi — dai sistemi di produzione al ripristino e alla risposta agli incidenti.", "button_text": "Scopri di più"}
        }
        for p_order, f in svc_pillars_it.items():
            p = ServicePillar.objects.filter(order=p_order).first()
            if p:
                for k, v in f.items(): setattr(p, f"{k}_it", {"format": "html", "content": v})
                p.save()

        return JsonResponse({"success": True, "message": "All CMS translations (Perfect Sync) completed successfully!"})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})
