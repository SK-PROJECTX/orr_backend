#!/usr/bin/env python
"""
Utility script to update Italian translations for CMS content in the database.
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()
from admin_portal.models_cms import (
    HowWeOperatePageContent, ProcessStep, ServicesPageContent, 
    ServiceStage, ServicePillar, HomePage, ServiceCard,
    ResourcesBlogsPageContent, ContentCard, BusinessSystemSection,
    ORRRoleSection, ORRReportSection, MessageStrip,
    StrategicAdvisoryPageContent, OperationalSystemsPageContent, 
    LivingSystemsPageContent, ApproachSection,
    Testimonial, BlogPost, ContactInfo, BusinessSystemCard,
    ProcessStage, LegacyPolicyPage, ContactPage
)

def update_translations():
    print("Updating Italian translations for CMS content...")

    # 1. Homepage
    homepage = HomePage.objects.filter(is_active=True).first()
    if homepage:
        homepage.hero_title_it = "Trasforma il tuo Business con ORR"
        homepage.hero_subtitle_it = "Consulenza Strategica, Innovazione Digitale e Soluzioni di Crescita Sostenibile"
        homepage.hero_cta_text_it = "Inizia Ora"
        homepage.about_title_it = "Chi è ORR"
        homepage.about_content_it = "Aiutiamo le organizzazioni a navigare sfide complesse..."
        homepage.services_title_it = "I Nostri Servizi"
        homepage.save()
        print("[OK] Homepage Italian translations updated")

    # 2. How We Operate Page
    how_we_operate = HowWeOperatePageContent.objects.filter(is_active=True).first()
    if how_we_operate:
        how_we_operate.hero_title_it = "Come Operiamo"
        how_we_operate.save()
        print("[OK] How We Operate Italian translations updated")

    # 3. Process Steps (How We Operate)
    steps_it = {
        '01': {
            'title': 'L\'Inizio',
            'bullet1': 'Una conversazione tranquilla.',
            'bullet2': 'Un problema.',
            'bullet3': 'Un punto di pressione.',
            'bullet4': 'Una storia che finalmente viene raccontata.',
            'description1': 'Ascoltiamo. Adeguatamente.',
            'description2': 'Non per diagnosticare troppo in fretta, non per impressionare —',
            'description3': 'ma per capire come respira effettivamente la vostra organizzazione.',
        },
        '02': {
            'title': 'La Prima Mappa',
            'subtitle': 'Dopo l\'incontro, il rumore si schiarisce.',
            'description': 'Apriamo una pagina bianca e iniziamo a disegnare la prima mappa della vostra organizzazione: dove le cose scorrono, dove si bloccano, dove l\'energia nascosta si disperde.',
            'bullet1': 'Nessuna rifinitura.',
            'bullet2': 'Nessuna proposta di vendita.',
            'bullet3': 'Solo pensiero per iscritto — il vostro dossier inizia qui.'
        },
        '05': {
            'title': 'Il Rapporto ORR',
            'subtitle': 'Raggiungete il punto decisionale.',
            'description': 'Ciò che ricevete non è decorazione — ma un modello strutturato e pronto per la decisione:',
            'bullet1': 'Cosa sta succedendo.',
            'bullet2': 'Perché sta succedendo.',
            'bullet3': 'Cosa deve cambiare ora.',
            'bullet4': 'Cosa può crescere più tardi.',
            'bullet5': 'E un modus operandi che lega tutto insieme.'
        }
    }

    for step_num, trans in steps_it.items():
        step = ProcessStep.objects.filter(step_number=step_num).first()
        if step:
            for field, value in trans.items():
                setattr(step, f"{field}_it", value)
            step.save()
            print(f"[OK] Process Step {step_num} Italian translations updated")

    # 4. Services Page Content
    services_page = ServicesPageContent.objects.filter(is_active=True).first()
    if services_page:
        services_page.hero_title_it = "Soluzioni ORR - Ascolta. Risolvi. Ottimizza."
        services_page.hero_subtitle_it = "Trattiamo la vostra organizzazione come un sistema intero — digitale, normativo e vivente. Ascoltiamo prima, poi progettiamo il giusto mix di consulenza, sistemi, IA e progetti sul campo in modo che possiate muovervi meglio e crescere anche in modo più intelligente."
        services_page.pillars_title_it = "I Tre Pilastri"
        services_page.business_gp_title_it = "ORR è il vostro Business GP per"
        services_page.business_gp_subtitle_it = "sistemi complessi — digitali e viventi."
        services_page.business_gp_description_it = "Ascoltiamo l'intera organizzazione, risolviamo con struttura e approfondimento, e ottimizziamo in modo che possiate crescere con fiducia."
        services_page.business_gp_button_text_it = "Contattaci"
        services_page.save()
        print("[OK] Services Page Italian translations updated")

    # 5. Service Pillars
    pillars_it = {
        'Digital Systems, Automation & AI': {
            'title': 'Sistemi Digitali, Automazione & IA',
            'description': 'SOP, flussi di lavoro, portali, dashboard e assistenti IA che fanno scorrere il lavoro con meno sforzo e meno sorprese.',
            'button_text': 'Scopri di più'
        },
        'Strategic Advisory & Compliance': {
            'title': 'Consulenza Strategica & Conformità',
            'description': 'Chiarezza breve e netta su regole, rischi e direzione — dalla regolamentazione ed ESG alle questioni biotech e ambientali.',
            'button_text': 'Scopri di più'
        },
        'Living Systems & Regeneration': {
            'title': 'Sistemi Viventi & Rigenerazione',
            'description': 'Supporto per terra, acqua, specie ed ecosistemi — dai sistemi di produzione al ripristino e alla risposta agli incidenti.',
            'button_text': 'Scopri di più'
        }
    }

    for title_en, trans in pillars_it.items():
        pillar = ServicePillar.objects.filter(title_en=title_en).first()
        if pillar:
            pillar.title_it = trans['title']
            pillar.description_it = trans['description']
            pillar.button_text_it = trans['button_text']
            pillar.save()
            print(f"[OK] Service Pillar '{title_en}' Italian translations updated")

    # 6. Resources & Blogs Page
    resources_page = ResourcesBlogsPageContent.objects.filter(is_active=True).first()
    if resources_page:
        resources_page.hero_title_it = "Risorse e Portale Clienti"
        resources_page.hero_description1_it = "Il vostro quartier generale digitale per chiarezza aziendale, timeline e stato in tempo reale. Questo non è un blog tradizionale."
        resources_page.hero_description2_it = "Le nostre risorse sono organizzate attorno al portale clienti ORR — una dashboard dove potete leggere le FAQ, scaricare materiale, richiedere incontri e chattare con un operatore o consulente dal vivo."
        resources_page.hero_description3_it = "Invece di articoli sparsi, ricevete una guida strutturata che segue il nostro progetto dal vivo — i blog seguenti hanno approfondimenti, how-to — e avvisi in tempo reale. Tutto è organizzato attorno alla gestione dei progetti in tempo reale, ai sistemi di marketing IA e all'implementazione."
        resources_page.hero_button1_text_it = "Richiedi l'accesso al portale clienti"
        resources_page.hero_button2_text_it = "Scopri come operiamo"
        resources_page.save()
        print("[OK] Resources & Blogs Page Italian translations updated")

    # 7. Content Cards (Blogs)
    for card in ContentCard.objects.all():
        if "Mobile Apps & PWAs" in str(card.title):
            card.title_it = "App Mobile & PWA per Assicuratori Maltesi: Aumentare il Coinvolgimento | Born Digital"
            card.badge_it = "Articolo"
            card.save()
            print(f"[OK] Content Card '{card.title}' updated")
        elif "Content Title" in str(card.title):
            card.title_it = "Titolo del Contenuto"
            card.badge_it = "Blog"
            card.save()
            print(f"[OK] Content Card '{card.title}' updated")

    # 8. Service Pillar Pages - Strategic Advisory
    strategic = StrategicAdvisoryPageContent.objects.filter(is_active=True).first()
    if strategic:
        strategic.hero_title_it = "Consulenza Strategica & Conformità"
        strategic.hero_subtitle_it = "Portiamo chiarezza alla complessità. Dai framework normativi e di sostenibilità alla consulenza biotecnologica e di conformità, i nostri esperti guidano i clienti attraverso scenari in continua evoluzione con fiducia."
        strategic.hero_description_it = "Il nostro approccio combina una profonda conoscenza tecnica con la lungimiranza strategica, garantendo che ogni iniziativa sia conforme, sostenibile e orientata alla crescita."
        strategic.services_title_it = "I Nostri Servizi Strategici"
        strategic.service_1_title_it = "Conformità Normativa"
        strategic.service_1_description_it = "Navigate nei complessi framework normativi con fiducia"
        strategic.service_2_title_it = "ESG & Sostenibilità"
        strategic.service_2_description_it = "Costruite pratiche commerciali sostenibili che guidano la crescita"
        strategic.service_3_title_it = "Gestione del Rischio"
        strategic.service_3_description_it = "Identificate e mitigate i rischi aziendali in modo proattivo"
        strategic.process_title_it = "Il Nostro Processo Strategico"
        strategic.process_description_it = "Come il vostro Medico di Medicina Generale (GP) aziendale, diagnostichiamo le sfide di conformità e prescriviamo soluzioni strategiche su misura per il contesto unico della vostra organizzazione."
        strategic.cta_title_it = "Pronti a Trasformare la vostra Strategia?"
        strategic.cta_description_it = "Discutiamo di come i nostri servizi di consulenza strategica possano aiutare la vostra organizzazione a prosperare."
        strategic.cta_button_text_it = "Inizia Ora"
        strategic.save()
        print("[OK] Strategic Advisory Page Italian translations updated")

    # 9. Operational Systems Page
    operational = OperationalSystemsPageContent.objects.filter(is_active=True).first()
    if operational:
        operational.hero_title_it = "Sistemi Operativi & Infrastruttura"
        operational.hero_subtitle_it = "Progettiamo, costruiamo e ottimizziamo i sistemi che alimentano le organizzazioni moderne. Che si tratti di creare SOP, strutturare flussi di lavoro o coordinare configurazioni complesse."
        operational.hero_description_it = "Trasformiamo le operazioni in ecosistemi ben funzionanti. La nostra rete fidata di costruttori e specialisti tecnologici offre affidabilità dalla pianificazione all'esecuzione."
        operational.services_title_it = "I Nostri Servizi Operativi"
        operational.service_1_title_it = "Ottimizzazione dei Processi"
        operational.service_1_description_it = "Semplificate i flussi di lavoro ed eliminate i colli di bottiglia operativi"
        operational.service_2_title_it = "Integrazione dei Sistemi"
        operational.service_2_description_it = "Collegate i vostri strumenti e piattaforme per operazioni senza intoppi"
        operational.service_3_title_it = "Configurazione dell'Infrastruttura"
        operational.service_3_description_it = "Costruite solide basi operative scalabili"
        operational.cta_title_it = "Pronti a Ottimizzare le vostre Operazioni?"
        operational.cta_button_text_it = "Inizia Ora"
        operational.save()
        print("[OK] Operational Systems Page Italian translations updated")

    # 10. Living Systems Page
    living = LivingSystemsPageContent.objects.filter(is_active=True).first()
    if living:
        living.hero_title_it = "Sistemi Viventi & Rigenerazione"
        living.hero_subtitle_it = "Supporto per terra, acqua, specie ed ecosistemi — dai sistemi di produzione al ripristino e alla risposta agli incidenti."
        living.hero_description_it = "Aiutiamo le organizzazioni a integrare pratiche rigenerative che favoriscono sia i risultati aziendali che la salute ambientale."
        living.services_title_it = "I Nostri Servizi Rigenerativi"
        living.service_1_title_it = "Ripristino dell'Ecosistema"
        living.service_1_description_it = "Ripristinate e rigenerate i sistemi naturali per una sostenibilità a lungo termine"
        living.service_2_title_it = "Produzione Sostenibile"
        living.service_2_description_it = "Progettate sistemi di produzione che lavorano con i processi naturali"
        living.service_3_title_it = "Monitoraggio Ambientale"
        living.service_3_description_it = "Tracciate e misurate l'impatto ambientale e il recupero"
        living.cta_title_it = "Pronti a Rigenerare il vostro Impatto?"
        living.cta_button_text_it = "Inizia Ora"
        living.save()
        print("[OK] Living Systems Page Italian translations updated")

    # 11. Generic Homepage Sections
    biz_sys = BusinessSystemSection.objects.filter(is_active=True).first()
    if biz_sys:
        biz_sys.title_it = "L'Azienda come Sistema Vivente"
        biz_sys.subtitle_it = "Pensate alla vostra organizzazione come a un corpo"
        biz_sys.card_1_title_it = "Sistema Nervoso"
        biz_sys.card_1_description_it = "Comunicazione, flusso di dati e percorsi decisionali"
        biz_sys.card_2_title_it = "Sistema Circolatorio"
        biz_sys.card_2_description_it = "Flusso di cassa, distribuzione delle risorse e scambio di valore"
        biz_sys.card_3_title_it = "Sistema Immunitario"
        biz_sys.card_3_description_it = "Gestione del rischio, conformità e misure protettive"
        biz_sys.save()
        print("[OK] Business System Section Italian translations updated")

    orr_role = ORRRoleSection.objects.filter(is_active=True).first()
    if orr_role:
        orr_role.title_it = "Il Ruolo di ORR"
        orr_role.description_it = "Agiamo come medici specialisti per la fisiologia della vostra azienda, ma partiamo dai vostri sintomi e dalle vostre priorità. Controlliamo la salute del vostro sistema, diagnostichiamo i problemi e co-progettiamo soluzioni che le vostre persone possano effettivamente utilizzare, mantenendo tutto funzionante nel tempo."
        orr_role.save()
        print("[OK] ORR Role Section Italian translations updated")

    strip = MessageStrip.objects.filter(is_active=True).first()
    if strip:
        strip.message_it = "Le aziende prosperano come organismi viventi quando tutti i loro sistemi lavorano insieme *attorno ai reali bisogni umani*. ORR mantiene la vostra 'fisiologia aziendale' in condizioni ottimali — allineando operazioni, comunicazione, flusso di cassa, conformità, dati e progetti attorno alle persone che servite."
        strip.save()
        print("[OK] Message Strip Italian translations updated")

    report = ORRReportSection.objects.filter(is_active=True).first()
    if report:
        report.title_it = "Cosa Ricevete: Il Rapporto ORR"
        report.subtitle_it = "Dopo il primo incontro, ricevete un rapporto ORR pronto per la decisione, progettato per essere immediatamente utile all'interno della vostra organizzazione."
        report.feature_1_it = "spiega la vostra situazione nella vostra lingua,"
        report.feature_2_it = "evidenzia problemi chiave e rischi che influenzano i vostri clienti e team"
        report.feature_3_it = "propone soluzioni rapide e miglioramenti a lungo termine che rispettano i vostri vincoli"
        report.feature_4_it = "mostra dove la consulenza, i sistemi digitali/IA o il lavoro sui sistemi viventi avranno il massimo impatto"
        report.save()
        print("[OK] ORR Report Section Italian translations updated")

    # 12. Approach Section
    approach = ApproachSection.objects.filter(is_active=True).first()
    if approach:
        approach.title_it = "L'Approccio ORR"
        approach.paragraph_1_it = "Proprio come un medico di base esperto, partiamo dalla vostra storia, non dal nostro framework. Ci prendiamo il tempo per capire come funziona realmente la vostra azienda prima di prescrivere qualsiasi cosa."
        approach.paragraph_2_it = "Non siamo un consulente solitario — siamo un livello di coordinamento centrale con una rete distribuita alle spalle. Quando necessario, attingiamo a specialisti in vari continenti, ma avrete sempre un unico punto di contatto: ORR, focalizzato su ciò che è meglio per voi."
        approach.paragraph_3_it = "Sistemiamo ciò che vi rallenta, rafforziamo i sistemi in base al modo in cui le vostre persone lavorano effettivamente e, quando è necessario un contributo più profondo, lo introduciamo al momento giusto — sempre al servizio dei vostri obiettivi."
        approach.save()
        print("[OK] Approach Section Italian translations updated")

    # 13. Service Cards
    for card in ServiceCard.objects.all():
        if "Strategic Advisory" in str(card.title):
            card.title_it = "Consulenza Strategica & Conformità"
            card.description_it = "Chiarezza su regole, rischi e direzione."
            card.save()
        elif "Digital Systems" in str(card.title):
            card.title_it = "Sistemi Digitali & IA"
            card.description_it = "Automazione e flussi di lavoro intelligenti."
            card.save()
        elif "Living Systems" in str(card.title):
            card.title_it = "Sistemi Viventi & Rigenerazione"
            card.description_it = "Supporto per ecosistemi e sostenibilità."
            card.save()
        print(f"[OK] Service Card '{card.title}' updated")

    # 14. Contact Page
    contact_page = ContactPage.objects.filter(is_active=True).first()
    if contact_page:
        contact_page.hero_title_it = "Contattaci"
        contact_page.contact_info_title_it = "Informazioni di Contatto"
        contact_page.contact_info_subtitle_it = "Scrivici per iniziare una conversazione!"
        contact_page.first_name_label_it = "Nome"
        contact_page.last_name_label_it = "Cognome"
        contact_page.email_label_it = "Email"
        contact_page.phone_label_it = "Numero di Telefono"
        contact_page.subject_label_it = "Seleziona Oggetto?"
        contact_page.message_label_it = "Messaggio"
        contact_page.submit_button_text_it = "Invia Messaggio"
        contact_page.save()
        print("[OK] Contact Page Italian translations updated")

    # 15. Legacy & Policy Page
    legacy = LegacyPolicyPage.objects.filter(is_active=True).first()
    if legacy:
        legacy.hero_title_it = "Legacy & Policy"
        legacy.hero_description_it = "Le nostre policy e il nostro impegno per un futuro sostenibile."
        legacy.save()
        print("[OK] Legacy & Policy Page Italian translations updated")

    print("\nTranslation update complete!")

if __name__ == '__main__':
    update_translations()
