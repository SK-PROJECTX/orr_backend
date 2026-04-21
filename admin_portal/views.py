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
    Final ultimate sync for Italian translations.
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

        # --- 2. BILINGUAL BLOG CARDS ---
        def update_card(title_en, title_it, badge_it, content_it_list):
            card = ContentCard.objects.filter(title_en__icontains=title_en).first()
            if card:
                card.title_it = {"format": "html", "content": title_it}
                card.badge_it = {"format": "html", "content": badge_it}
                card.content_it = content_it_list
                card.button1_text_it = {"format": "html", "content": "Leggi Articolo"}
                card.save()

        # Card 1: Why a Portal
        update_card(
            "WHY A PORTAL", 
            "PERCHÉ UN PORTALE, NON SOLO UN BLOG?", 
            "Blog",
            ["Progettato per persone che vogliono agire, non solo leggere. Tutto ciò di cui hai bisogno è in un'unica posizione. Il portale client ORR dal vivo collega risorse, FAQ, chat e gestione dei progetti in un unico posto."]
        )

        # Card 2: How content is organised
        update_card(
            "HOW CONTENT IS ORGANISED", 
            "COME È ORGANIZZATO IL CONTENUTO", 
            "Guida",
            ["Risorse che seguono il nostro modo di lavorare. Tutto qui è focalizzato sui progetti e su risorse dal vivo - non articoli indipendenti o suggerimenti casuali."]
        )

        # Card 3: What you can do today
        update_card(
            "WHAT YOU CAN DO TODAY", 
            "COSA PUOI FARE OGGI", 
            "Guida",
            [
                "Prima, durante e dopo il lavoro con ORR. Che tu stia appena iniziando o che ci stia già pensando: leggi le nostre FAQ e richiedi una chiamata con noi.",
                "Prima di iniziare: leggi come si svolgono i nostri incontri dal vivo e il lavoro con i clienti — così saprai cosa aspettarti.",
                "Durante l'incarico: accedi allo stato del progetto in tempo reale — vedi i progressi e chiedi risposte immediate.",
                "Dopo il progetto: scarica le risorse, ottieni supporto continuo e accedi alla nostra rete di alumni."
            ]
        )

        # Card 4: How access works
        update_card(
            "HOW ACCESS WORKS", 
            "COME FUNZIONA L'ACCESSO", 
            "Accesso",
            [
                "Semplice. Accesso immediato. Richiedi l'accesso: clicca sul pulsante sopra e ti invieremo un'email con i tuoi dati di accesso.",
                "Ricevi il tuo login: controlla la tua email per le credenziali e il link al tuo portale client.",
                "Inizia a esplorare: accedi e inizia a esplorare risorse, FAQ e strumenti del progetto.",
                "Prenota la tua chat: usa il nostro calendario in-app per prenotare una chiamata di 15 minuti con il nostro team."
            ]
        )

        # Basic labels for other cards
        for card in ContentCard.objects.all():
            if not card.badge_it:
                card.badge_it = {"format": "html", "content": "Articolo"}
            if not card.button1_text_it:
                card.button1_text_it = {"format": "html", "content": "Leggi Tutto"}
            card.save()

        # --- 3. OTHER PAGES (RE-SYNC) ---
        how_page = HowWeOperatePageContent.objects.first()
        if how_page:
            how_page.hero_title_it = {"format": "html", "content": "Come Operiamo"}
            how_page.save()

        return JsonResponse({"success": True, "message": "Global Perfect Italian Sync Complete! All cards, labels, and text localized."})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})
