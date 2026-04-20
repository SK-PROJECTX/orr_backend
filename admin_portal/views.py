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
            1: {"title": "L'Inizio", "bullet1": "Una conversazione tranquilla.", "description1": "Ascoltiamo. In modo approfondito."},
            2: {"title": "La Prima Mappa", "subtitle": "Dopo l'incontro, il rumore si placa.", "description": "Apriamo una pagina bianca e iniziamo a disegnare la prima mappa della tua organizzazione."},
            3: {"title": "L'Approfondimento", "subtitle": "La mappa si affina.", "description": "Attingiamo alle giuste forme di intelligenza."},
            4: {"title": "La Seconda Conversazione", "subtitle": "Ora le domande si fanno più affilate."},
            5: {"title": "Il Rapporto ORR", "subtitle": "Arrivi al punto della decisione.", "description1": "Un progetto che si regge da solo."},
            6: {"title": "L'Architettura degli Incontri", "subtitle": "Dietro le quinte, il ritmo è semplice:"},
            7: {"title": "La Scelta", "subtitle": "Con il rapporto in mano, scegli il percorso:", "wordbreak": "OPPURE"},
            8: {"title": "Il Portale", "subtitle": "Se rimani con noi, il lavoro cambia marcia."},
            9: {"title": "La Filosofia alla Base", "description1": "È il metodo del Business GP."},
            10: {"title": "L'Invito", "description1": "È più lento all'inizio, più veloce alla fine.", "button_text": "Prenota il Tuo Primo Incontro", "button_text2": "Esplora i nostri servizi", "button_text3": "Accedi al Portale Client"}
        }
        for s_id, f in steps_it.items():
            s = ProcessStep.objects.filter(id=s_id).first()
            if s:
                for k, v in f.items(): setattr(s, f"{k}_it", {"format": "html", "content": v})
                s.save()

        # --- 3. SERVICES PAGE CONTENT ---
        svc_page_it = {
            "hero_title": "ORR Solutions - Ascolta. Risolvi. Ottimizza.",
            "hero_subtitle": "Trattiamo la tua organizzazione come un intero sistema: digitale, normativo e vivente.",
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
            1: {"title": "FASE 1 - SCOPERTA", "subtitle": "Ascolta.", "description": "Iniziamo in modo semplice: una conversazione tranquilla e una scansione rapida della tua realtà."},
            2: {"title": "FASE 2 - DIAGNOSI", "subtitle": "Pensa. Poi ascolta di nuovo.", "description": "Trasformiamo i sintomi in una mappa chiara di problemi e opportunità attraverso i tre pilastri."},
            3: {"title": "FASE 3 - PROGETTAZIONE", "subtitle": "Progetta.", "description": "Progettiamo strutture pratiche, non presentazioni teoriche."},
            4: {"title": "FASE 4 - IMPLEMENTAZIONE", "subtitle": "Risolvi nella pratica.", "description": "Il progetto diventa realtà con un'implementazione guidata."},
            5: {"title": "FASE 5 - CRESCITA", "subtitle": "Ottimizza.", "description": "Una volta che i sistemi sono attivi, continuiamo a farli imparare."}
        }
        for st_id, f in svc_stages_it.items():
            st = ServiceStage.objects.filter(stage_number=st_id).first()
            if st:
                for k, v in f.items(): setattr(st, f"{k}_it", {"format": "html", "content": v})
                st.save()

        # --- 5. SERVICE PILLARS ---
        svc_pillars_it = {
            1: {"title": "Consulenza Strategica e Conformità", "description": "Chiarezza normativa, quadri ESG e sostenibilità, biotecnologie e questioni ambientali.", "button_text": "Esplora Consulenza e Conformità"},
            2: {"title": "Sistemi Digitali, Automazione e AI", "description": "SOP, flussi di lavoro, portali, dashboard e strumenti assistiti dall'AI progettati intorno alle abitudini del tuo team.", "button_text": "Esplora Sistemi Digitali e AI"},
            3: {"title": "Sistemi Viventi e Rigenerazioni", "description": "Supporto per terra, acqua, specie ed ecosistemi - su misura per i tuoi siti, i tuoi rischi e le tue opportunità.", "button_text": "Esplora Sistemi Viventi e Rigenerazione"}
        }
        for p_id, f in svc_pillars_it.items():
            p = ServicePillar.objects.filter(order=p_id).first()
            if p:
                for k, v in f.items(): setattr(p, f"{k}_it", {"format": "html", "content": v})
                p.save()

        return JsonResponse({"success": True, "message": "All CMS translations (How We Operate & Services) synced successfully!"})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})
