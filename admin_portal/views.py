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
    Consolidated view to trigger Italian translation sync for all CMS pages.
    Visit: /admin-portal/sync-it-translations-secret/
    """
    try:
        # --- 1. HOW WE OPERATE PAGE ---
        how_page = HowWeOperatePageContent.objects.first()
        if how_page:
            how_page.hero_title_it = {"format": "html", "content": "Come Operiamo"}
            how_page.meta_title_it = {"format": "html", "content": "Metodologia ORR Solutions - Come Operiamo"}
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
            10: {"title": "L'Invito", "description1": "È più lento all'inizio, più veloce alla fine.", "button_text": "Prenota il Tuo Incontro"}
        }
        for s_id, f in steps_it.items():
            s = ProcessStep.objects.filter(id=s_id).first()
            if s:
                for k, v in f.items(): setattr(s, f"{k}_it", {"format": "html", "content": v})
                s.save()

        # --- 3. SERVICES PAGE CONTENT ---
        svc_page = ServicesPageContent.objects.first()
        if svc_page:
            svc_page.hero_title_it = {"format": "html", "content": "ORR Solutions - Ascolta. Risolvi. Ottimizza."}
            svc_page.hero_subtitle_it = {"format": "html", "content": "Trattiamo la tua organizzazione come un intero sistema: digitale, normativo e vivente. Ascoltiamo prima di tutto, poi progettiamo il giusto mix di consulenza, sistemi, AI e progetti sul campo in modo che tu possa muoverti meglio e crescere in modo più intelligente."}
            svc_page.pillars_title_it = {"format": "html", "content": "I Tre Pilastri"}
            svc_page.business_gp_title_it = {"format": "html", "content": "ORR è il tuo Business GP per"}
            svc_page.business_gp_description_it = {"format": "html", "content": "Ascoltiamo l'intera organizzazione, risolviamo con struttura e visione, e ottimizziamo affinché tu possa crescere con fiducia."}
            svc_page.business_gp_button_text_it = {"format": "html", "content": "Contattaci"}
            svc_page.save()

        # --- 4. SERVICE STAGES (1-5) ---
        svc_stages_it = {
            1: {"title": "FASE 1 - SCOPERTA", "subtitle": "Ascolta.", "focus_content": "Ci concentriamo su:\n• Il tuo contesto, le persone e le pressioni\n• Rischi normativi, operativi e ambientali", "button_text": "Iscriviti"},
            2: {"title": "FASE 2 - DIAGNOSI", "subtitle": "Pensa. Poi ascolta.", "focus_content": "Cosa succede qui:\n• Mappatura dei processi\n• Revisione di conformità e rischio", "button_text": "Scopri di Più"},
            3: {"title": "FASE 3 - PROGETTAZIONE", "subtitle": "Progetta.", "focus_content": "Output Tipici:\n• SOP e flussi di lavoro\n• Stack tecnologico e AI", "button_text": "Iscriviti"},
            4: {"title": "FASE 4 - IMPLEMENTAZIONE", "subtitle": "Risolvi.", "focus_content": "L'implementazione include:\n• Configurazione amministrativa\n• Dashboard KPI", "button_text": "Contattaci"},
            5: {"title": "FASE 5 - CRESCITA", "subtitle": "Ottimizza.", "focus_content": "Supporto alla crescita:\n• Analisi continua dati\n• Revisioni trimestrali", "button_text": "Iscriviti"}
        }
        for st_num, f in svc_stages_it.items():
            st = ServiceStage.objects.filter(stage_number=st_num).first()
            if st:
                for k, v in f.items(): setattr(st, f"{k}_it", {"format": "html", "content": v})
                st.save()

        # --- 5. RESOURCES & BLOGS PAGE ---
        res_page = ResourcesBlogsPageContent.objects.first()
        if res_page:
            res_page.hero_title_it = {"format": "html", "content": "Risorse & Portale Client"}
            res_page.hero_description1_it = {"format": "html", "content": "Il tuo quartier generale digitale per la chiarezza aziendale. Questo non è un blog tradizionale."}
            res_page.hero_button1_text_it = {"format": "html", "content": "Richiedi l'accesso al portale client"}
            res_page.save()

        # --- 6. CONTACT PAGE CONTENT ---
        con_page = ContactPageContent.objects.first()
        if con_page:
            con_page.hero_title_it = {"format": "html", "content": "Contattaci"}
            con_page.contact_info_title_it = {"format": "html", "content": "Informazioni di Contatto"}
            con_page.first_name_label_it = {"format": "html", "content": "Nome"}
            con_page.last_name_label_it = {"format": "html", "content": "Cognome"}
            con_page.email_label_it = {"format": "html", "content": "Email"}
            con_page.phone_label_it = {"format": "html", "content": "Numero di Telefono"}
            con_page.subject_label_it = {"format": "html", "content": "Oggetto"}
            con_page.message_label_it = {"format": "html", "content": "Messaggio"}
            con_page.submit_button_text_it = {"format": "html", "content": "Invia Messaggio"}
            con_page.save()

        return JsonResponse({"success": True, "message": "All CMS translations (Full Site: How We Operate, Services, Resources, Contact) completed successfully!"})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})
