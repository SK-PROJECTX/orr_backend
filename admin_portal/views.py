from django.shortcuts import render
from django.http import JsonResponse
from admin_portal.models import (
    HowWeOperatePageContent, ProcessStep, 
    ServicesPageContent, ServiceStage, ServicePillar,
    ResourcesBlogsPageContent, ContentCard,
    ContactPageContent,
    Testimonial, MessageStrip
)

def sync_cms_it_view(request):
    """
    Fixed ultimate sync for Italian translations.
    Resolves 'dict' object has no attribute 'upper' error.
    Visit: /admin-portal/sync-it-translations-secret/
    """
    try:
        # --- 1. HERO - RESOURCES & BLOGS ---
        res_page = ResourcesBlogsPageContent.objects.first()
        if res_page:
            res_page.hero_title_it = {"format": "html", "content": "Risorse & Portale Client"}
            res_page.hero_description1_it = {"format": "html", "content": "Il tuo quartier generale digitale per la chiarezza aziendale, le tempistiche e lo stato in tempo reale. Questo non è un blog tradizionale."}
            res_page.hero_description2_it = {"format": "html", "content": "Le nostre risorse sono organizzate attorno al portale client ORR — un cruscotto dove puoi leggere le FAQ, scaricare materiale, richiedere incontri e chattare con un operatore o consulente dal vivo."}
            res_page.hero_description3_it = {"format": "html", "content": "Invece di articoli sparsi, ricevi una guida strutturata che segue il nostro progetto dal vivo — i blog contengono approfondimenti, guide pratiche e avvisi in tempo reale. Tutto è organizzato intorno alla gestione dei progetti e all'implementazione AI."}
            res_page.hero_button1_text_it = {"format": "html", "content": "Richiedi l'accesso al portale client"}
            res_page.hero_button2_text_it = {"format": "html", "content": "Scopri come operiamo"}
            res_page.save()

        # --- 2. BILINGUAL BLOG CARDS (Safe Matching) ---
        cards = ContentCard.objects.all()
        for card in cards:
            # Extract content string from title_en dict safely
            title_data = card.title_en or {}
            if isinstance(title_data, dict):
                title_text = title_data.get('content', '')
            else:
                title_text = str(title_data)
                
            title_en = title_text.upper()
            
            # Card: WHY A PORTAL
            if "WHY A PORTAL" in title_en:
                card.title_it = {"format": "html", "content": "PERCHÉ UN PORTALE, NON SOLO UN BLOG?"}
                card.badge_it = {"format": "html", "content": "Blog"}
                card.content_it = ["Progettato per persone che vogliono agire, non solo leggere. Tutto ciò di cui hai bisogno è in un'unica posizione. Il portale client ORR dal vivo collega risorse, FAQ, chat e gestione dei progetti in un unico posto."]
            
            # Card: HOW CONTENT IS ORGANISED
            elif "CONTENT IS ORGANISED" in title_en or "CONTENT IS ORGANIZED" in title_en:
                card.title_it = {"format": "html", "content": "COME È ORGANIZZATO IL CONTENUTO"}
                card.badge_it = {"format": "html", "content": "Guida"}
                card.content_it = ["Risorse che seguono il nostro modo di lavorare. Tutto qui è focalizzato sui progetti e su risorse dal vivo — non articoli indipendenti o suggerimenti casuali."]
            
            # Card: WHAT YOU CAN DO TODAY
            elif "WHAT YOU CAN DO TODAY" in title_en:
                card.title_it = {"format": "html", "content": "COSA PUOI FARE OGGI"}
                card.badge_it = {"format": "html", "content": "Guida"}
                card.content_it = [
                    "Prima, durante e dopo il lavoro con ORR. Che tu stia appena iniziando o che ci stia già pensando: leggi le nostre FAQ e richiedi una chiamata con noi.",
                    "Prima di iniziare: leggi come si svolgono i nostri incontri dal vivo e il lavoro con i clienti — così saprai cosa aspettarti quando inizieremo a lavorare insieme.",
                    "Durante l'incarico: accedi allo stato del progetto in tempo reale — vedi i progressi, fai domande e ottieni risposte immediate dal nostro team.",
                    "Dopo il completamento del progetto: scarica le risorse dai lavori completati, ottieni supporto continuo e accedi alla nostra rete di alumni.",
                    "Accedi alle risorse su temi chiave dello sviluppo, della gestione dei progetti e della crescita del business."
                ]
            
            # Card: HOW ACCESS WORKS
            elif "HOW ACCESS WORKS" in title_en:
                card.title_it = {"format": "html", "content": "COME FUNZIONA L'ACCESSO"}
                card.badge_it = {"format": "html", "content": "Accesso"}
                card.content_it = [
                    "Semplice. Accesso immediato. Richiedi l'accesso: clicca sul pulsante sopra e ti invieremo un'email con i tuoi dati di accesso.",
                    "Ricevi il tuo login: controlla la tua email per le credenziali e il link al tuo portale client.",
                    "Inizia a esplorare: accedi e inizia a esplorare risorse, FAQ e strumenti del progetto.",
                    "Prenota la tua prima chat: usa il nostro calendario in-app per prenotare una chiamata di 15 minuti con il nostro team per discutere del tuo progetto e dei prossimi passi.",
                    "Richiedi il tuo primo progetto: invia la tua prima richiesta di progetto direttamente attraverso il portale e inizia il nostro processo in 4 fasi."
                ]

            # General fallbacks
            if not card.badge_it:
                card.badge_it = {"format": "html", "content": "Articolo"}
            card.button1_text_it = {"format": "html", "content": "Leggi Articolo"}
            card.save()

        # --- 3. FAQs (NEW) ---
        faqs = FAQ.objects.all()
        for faq in faqs:
            q_en = str(faq.question).upper()
            
            if "WHAT DOES IT MEAN" in q_en or "BUSINESS GP" in q_en:
                faq.question_it = {"format": "html", "content": "Cosa significa che ORR è un Medico di Medicina Generale (GP) aziendale?"}
                faq.answer_it = {"format": "html", "content": "Lavoriamo come un medico di base per la vostra organizzazione. Iniziamo ascoltando, comprendiamo il vostro contesto e i vostri vincoli, quindi introduciamo il giusto mix di competenze in ambito di consulenza, sistemi, IA e natura per trattare le cause profonde — sempre ancorati a ciò che conta di più per voi e per i vostri clienti."}
            elif "FIRST MEETING" in q_en:
                faq.question_it = {"format": "html", "content": "Cosa succede nel primo incontro?"}
                faq.answer_it = {"format": "html", "content": "Nel nostro primo incontro, ci concentriamo sulla comprensione della vostra situazione attuale, delle sfide e degli obiettivi. Discuteremo il vostro contesto aziendale, identificheremo i principali punti critici ed esploreremo come appare il successo per voi. Questo ci aiuta a creare un rapporto ORR su misura con raccomandazioni attuabili."}
            elif "ORR REPORT" in q_en:
                faq.question_it = {"format": "html", "content": "Cos'è il rapporto ORR?"}
                faq.answer_it = {"format": "html", "content": "Il rapporto ORR è un'analisi completa che forniamo dopo il nostro primo incontro. Delinea i problemi chiave che interessano il vostro business, propone soluzioni rapide e miglioramenti a lungo termine, e mostra dove il nostro lavoro di consulenza, sui sistemi digitali o sui sistemi viventi avrà il maggior impatto sulla vostra organizzazione."}
            elif "COST" in q_en or "HOW MUCH" in q_en:
                faq.question_it = {"format": "html", "content": "Quanto costano gli incontri e il rapporto?"}
                faq.answer_it = {"format": "html", "content": "I nostri incontri sono fatturati a €45/ora su base pro-rata, progettati per essere brevi, mirati e densi di valore. Il costo del rapporto ORR parte da €220, sebbene il costo finale dipenda dalla complessità della vostra situazione e dei vostri requisiti."}
            elif "KEEP WORKING" in q_en or "AFTER THE REPORT" in q_en:
                faq.question_it = {"format": "html", "content": "Devo continuare a lavorare con ORR dopo il rapporto?"}
                faq.answer_it = {"format": "html", "content": "Niente affatto. Il rapporto ORR è progettato per fornire valore sia che continuiate a lavorare con noi o meno. Include raccomandazioni attuabili che potete implementare in autonomia. Tuttavia, siamo disponibili a supportare l'implementazione se sceglierete di continuare la nostra collaborazione."}
            faq.save()

        # --- 4. OTHER PAGES (RE-SYNC) ---
        how_page = HowWeOperatePageContent.objects.first()
        if how_page:
            how_page.hero_title_it = {"format": "html", "content": "Come Operiamo"}
            how_page.save()

        # ORR Role Section
        orr_role = ORRRoleSection.objects.first()
        if orr_role:
            orr_role.title_it = {"format": "html", "content": "Il Ruolo di ORR"}
            orr_role.description_it = {"format": "html", "content": "Agiamo come medici specialisti per la fisiologia della vostra azienda, ma partiamo dai vostri sintomi e dalle vostre priorità. Controlliamo la salute del vostro sistema, diagnostichiamo i problemi e co-progettiamo soluzioni che le vostre persone possano effettivamente utilizzare, mantenendo tutto funzionante nel tempo."}
            orr_role.save()

        return JsonResponse({"success": True, "message": "Global Perfect Italian Sync Complete! No errors."})
    except Exception as e:
        import traceback
        return JsonResponse({"success": False, "error": str(e), "traceback": traceback.format_exc()})
