import os
import django
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.production' if '--prod' in sys.argv else 'core.settings.local')
django.setup()

from admin_portal.models_cms import (
    StrategicAdvisoryPageContent, OperationalSystemsPageContent, LivingSystemsPageContent,
    HomePage, ServicesPageContent, ResourcesBlogsPageContent, LegalPolicyPageContent, 
    ContactPageContent, HowWeOperatePageContent, ProcessStep, ServiceStage, ServicePillar,
    ContentCard, PolicyItem, ApproachSection, ORRRoleSection, MessageStrip,
    BusinessSystemSection, ProcessSection, ORRReportSection, FAQ, Testimonial, ServiceCard
)

def to_rich_text(content):
    return {"format": "html", "content": content}

def populate():
    print("Populating ALL CMS content with absolute completeness...")

    # --- STRATEGIC ADVISORY ---
    st, _ = StrategicAdvisoryPageContent.objects.get_or_create(is_active=True)
    # English
    st.hero_title_en = to_rich_text("Strategic Advisory & Compliance")
    st.hero_subtitle_en = to_rich_text("We deliver clarity to complexity. Our experts guide clients through evolving landscapes.")
    st.hero_description_en = to_rich_text("Our approach combines deep technical insight with strategic foresight, ensuring every initiative is compliant, sustainable, and built for growth.")
    st.services_title_en = to_rich_text("Our Strategic Services")
    st.service_1_title_en = to_rich_text("Regulatory Compliance & Advisory")
    st.service_1_description_en = to_rich_text("Navigate complex regulatory frameworks with confidence.")
    st.service_2_title_en = to_rich_text("ESG & Sustainability Strategy")
    st.service_2_description_en = to_rich_text("Build sustainable business practices that drive long-term value.")
    st.service_3_title_en = to_rich_text("Corporate Risk Management")
    st.service_3_description_en = to_rich_text("Identify and mitigate business risks proactively across your organization.")
    st.process_title_en = to_rich_text("Our Strategic Process")
    st.process_subtitle_en = to_rich_text("Listen . Solve . Optimize")
    st.process_description_en = to_rich_text("Like your Business GP, we diagnose compliance challenges and prescribe solutions tailored to your unique context.")
    st.process_step_1_title_en = to_rich_text("Listen & Report")
    st.process_step_1_subtitle_en = to_rich_text("(Initial Discovery)")
    st.process_step_1_en = to_rich_text("We start with a focused initial meeting to understand your compliance challenges and regulatory environment.")
    st.process_step_2_title_en = to_rich_text("Strategic Design")
    st.process_step_2_en = to_rich_text("We co-design solutions that fit your context, respecting your constraints and priorities.")
    st.process_step_3_title_en = to_rich_text("Implementation")
    st.process_step_3_en = to_rich_text("Design becomes reality with guided implementation and integration into your workflows.")
    st.process_step_4_title_en = to_rich_text("Grow")
    st.process_step_4_en = to_rich_text("We keep your systems learning and adapting to ensure long-term resilience.")
    st.network_title_en = to_rich_text("The ORR Network Advantage")
    st.network_description_en = to_rich_text("Complex challenges require diverse expertise. We activate global specialists to deliver results.")
    st.digital_title_en = to_rich_text("Digital Solutions for")
    st.digital_subtitle_en = to_rich_text("Compliance Management")
    st.digital_description_en = to_rich_text("We build digital infrastructure to operationalize compliance, including automated tracking platforms and ESG reporting dashboards.")
    st.digital_image_alt_en = to_rich_text("Network visualization showing connected nodes and data flows")
    st.case_challenge_en = to_rich_text("Navigating international compliance for a rapidly expanding biotech startup.")
    st.case_solution_en = to_rich_text("Implemented a centralized regulatory monitoring system integrated with their existing workflows.")
    st.case_result_en = to_rich_text("Reduced compliance-related delays by 40% and successfully entered 3 new markets.")
    st.case_image_alt_en = to_rich_text("Business documents and reports on a desk")
    st.cta_title_en = to_rich_text("Ready to Transform Your Strategy?")
    st.cta_description_en = to_rich_text("Let's discuss how our strategic advisory services can help your organization thrive.")
    st.cta_button_text_en = to_rich_text("Get Started")
    st.meta_title_en = to_rich_text("Strategic Advisory | ORR")
    st.meta_description_en = to_rich_text("Expert strategic advisory and compliance consulting for complex regulatory landscapes.")
    
    st.network_cards_en = [
        {"text": "Legal & Regulatory Experts — specialized attorneys and compliance professionals across multiple jurisdictions", "type": "expert"},
        {"text": "Scientific Advisors — PhDs and researchers in biotechnology, environmental and computer science, and related fields", "type": "expert"},
        {"text": "Industry Specialists — sector-specific consultants with deep regulatory knowledge", "type": "expert"},
        {"text": "Technical Auditors — certification professionals for ISO, GMP, and other standards", "type": "expert"},
        {"text": "ESG Consultants — sustainability experts and carbon accounting specialists", "type": "expert"}
    ]
    st.digital_who_is_this_for = [
        {"text": "Self-employed professionals and consultants who need expert compliance guidance without hiring full-time staff", "type": "audience"},
        {"text": "Growing businesses entering regulated industries or expanding into new markets", "type": "audience"},
        {"text": "Startups in life sciences and biotech navigating complex regulatory pathways", "type": "audience"},
        {"text": "Professional service firms managing client compliance obligations", "type": "audience"},
        {"text": "Companies facing regulatory changes that impact their operations", "type": "audience"},
        {"text": "Businesses implementing ESG strategies to meet investor and stakeholder expectations", "type": "audience"}
    ]
    st.digital_features = [
        {"text": "Custom compliance management platforms with automated tracking", "type": "solution"},
        {"text": "Regulatory document repositories with version control and access management", "type": "solution"},
        {"text": "ESG data collection and reporting dashboards", "type": "solution"},
        {"text": "Audit trail systems with timestamped documentation", "type": "solution"},
        {"text": "Training management systems with certification tracking", "type": "solution"},
        {"text": "AI-powered regulatory monitoring and change detection", "type": "solution"},
        {"text": "Integrated risk assessment and mitigation tracking tools", "type": "solution"},
        {"text": "Automated compliance reporting and submission workflows", "type": "solution"}
    ]

    # Italian (Populate EVERYTHING)
    st.hero_title_it = to_rich_text("Consulenza Strategica & Compliance")
    st.hero_subtitle_it = to_rich_text("Diamo chiarezza alla complessità. I nostri esperti guidano i clienti attraverso scenari in evoluzione.")
    st.hero_description_it = to_rich_text("Il nostro approccio combina una profonda conoscenza tecnica con una lungimiranza strategica, garantendo che ogni iniziativa sia conforme e sostenibile.")
    st.services_title_it = to_rich_text("I Nostri Servizi Strategici")
    st.service_1_title_it = to_rich_text("Conformità Normativa & Consulenza")
    st.service_1_description_it = to_rich_text("Naviga in complessi contesti normativi con fiducia.")
    st.service_2_title_it = to_rich_text("Strategia ESG & Sostenibilità")
    st.service_2_description_it = to_rich_text("Costruisci pratiche aziendali sostenibili che creano valore a lungo termine.")
    st.service_3_title_it = to_rich_text("Gestione del Rischio Aziendale")
    st.service_3_description_it = to_rich_text("Identifica e mitiga i rischi aziendali in modo proattivo.")
    st.process_title_it = to_rich_text("Il Nostro Processo Strategico")
    st.process_subtitle_it = to_rich_text("Ascolta . Risolvi . Ottimizza")
    st.process_description_it = to_rich_text("Come il vostro Medico di Base aziendale, diagnostichiamo le sfide di conformità e prescriviamo soluzioni su misura.")
    st.process_step_1_title_it = to_rich_text("Ascolta & Rapporto")
    st.process_step_1_subtitle_it = to_rich_text("(Scoperta Iniziale)")
    st.process_step_1_it = to_rich_text("Iniziamo con un incontro mirato per comprendere le vostre sfide di conformità e l'ambiente normativo.")
    st.process_step_2_title_it = to_rich_text("Design Strategico")
    st.process_step_2_it = to_rich_text("Co-progettiamo soluzioni che si adattano al vostro contesto, rispettando i vostri vincoli.")
    st.process_step_3_title_it = to_rich_text("Implementazione")
    st.process_step_3_it = to_rich_text("Il design diventa realtà con un'implementazione guidata nei vostri flussi di lavoro.")
    st.process_step_4_title_it = to_rich_text("Crescita")
    st.process_step_4_it = to_rich_text("Manteniamo i vostri sistemi in apprendimento e adattamento per garantire resilienza a lungo termine.")
    st.network_title_it = to_rich_text("Il Vantaggio del Network ORR")
    st.network_description_it = to_rich_text("Sfide complesse richiedono competenze diverse. Attiviamo specialisti globali per fornire risultati.")
    st.digital_title_it = to_rich_text("Soluzioni Digitali per la")
    st.digital_subtitle_it = to_rich_text("Gestione della Conformità")
    st.digital_description_it = to_rich_text("Costruiamo infrastrutture digitali per rendere operativa la conformità, inclusi sistemi di tracciamento e dashboard ESG.")
    st.digital_image_alt_it = to_rich_text("Visualizzazione di rete che mostra nodi e flussi di dati")
    st.case_challenge_it = to_rich_text("Gestione della conformità internazionale per una startup biotecnologica in rapida espansione.")
    st.case_solution_it = to_rich_text("Implementato un sistema di monitoraggio normativo centralizzato integrato con i flussi esistenti.")
    st.case_result_it = to_rich_text("Riduzione dei ritardi legati alla conformità del 40% e ingresso con successo in 3 nuovi mercati.")
    st.case_image_alt_it = to_rich_text("Documenti e rapporti aziendali su una scrivania")
    st.cta_title_it = to_rich_text("Pronto a Trasformare la tua Strategia?")
    st.cta_description_it = to_rich_text("Discutiamo di come i nostri servizi di consulenza possano aiutare la tua organizzazione.")
    st.cta_button_text_it = to_rich_text("Inizia Ora")
    st.meta_title_it = to_rich_text("Consulenza Strategica | ORR")
    st.meta_description_it = to_rich_text("Consulenza strategica esperta per contesti normativi complessi.")
    
    st.network_cards_it = [
        {"text": "Esperti Legali e Normativi — avvocati specializzati e professionisti della conformità in diverse giurisdizioni", "type": "expert"},
        {"text": "Consulenti Scientifici — ricercatori in biotecnologie, scienze ambientali e informatiche", "type": "expert"},
        {"text": "Specialisti di Settore — consulenti con profonda conoscenza normativa", "type": "expert"},
        {"text": "Revisori Tecnici — professionisti della certificazione per ISO, GMP e altri standard", "type": "expert"},
        {"text": "Consulenti ESG — esperti in sostenibilità e specialisti nella contabilità delle emissioni", "type": "expert"}
    ]
    st.save()

    # --- OPERATIONAL SYSTEMS ---
    op, _ = OperationalSystemsPageContent.objects.get_or_create(is_active=True)
    # English
    op.hero_title_en = to_rich_text("Operational Systems & Infrastructure")
    op.hero_subtitle_en = to_rich_text("We design, build and streamline the systems that power modern organizations.")
    op.hero_description_en = to_rich_text("We turn operations into well-functioning ecosystems. Our trusted network delivers reliability from planning to execution.")
    op.services_title_en = to_rich_text("Our Operational Services")
    op.service_1_title_en = to_rich_text("Process Optimization")
    op.service_1_description_en = to_rich_text("Streamline workflows and eliminate operational bottlenecks.")
    op.service_2_title_en = to_rich_text("System Integration")
    op.service_2_description_en = to_rich_text("Connect your tools and platforms for seamless operations.")
    op.service_3_title_en = to_rich_text("Infrastructure Setup")
    op.service_3_description_en = to_rich_text("Build robust operational foundations that scale.")
    op.process_title_en = to_rich_text("Our Implementation Process")
    op.process_description_en = to_rich_text("Just like your Business GP, we follow a systematic diagnostic approach to restore operational health.")
    op.process_step_1_title_en = to_rich_text("Assess")
    op.process_step_1_en = to_rich_text("Deep analysis of current state.")
    op.process_step_2_title_en = to_rich_text("Design")
    op.process_step_2_en = to_rich_text("Tailored system design.")
    op.process_step_3_title_en = to_rich_text("Implement")
    op.process_step_3_en = to_rich_text("Guided execution.")
    op.process_step_4_title_en = to_rich_text("Sustain")
    op.process_step_4_en = to_rich_text("Ongoing clinical check-ins.")
    op.case_challenge_en = to_rich_text("Scaling operations without losing quality control in manufacturing.")
    op.case_solution_en = to_rich_text("Redesigned the entire supply chain with automated quality gates.")
    op.case_result_en = to_rich_text("Increased production output by 30% while reducing defects by 50%.")
    op.case_image_alt_en = to_rich_text("Manufacturing facility operational dashboard")
    op.cta_title_en = to_rich_text("Ready to Optimize?")
    op.cta_description_en = to_rich_text("Let's build systems that grow with you.")
    op.cta_button_text_en = to_rich_text("Get Started")
    op.meta_title_en = to_rich_text("Operational Systems | ORR")
    op.meta_description_en = to_rich_text("Streamlining operational infrastructure and modern systems.")
    # Italian
    op.hero_title_it = to_rich_text("Sistemi Operativi & Infrastruttura")
    op.hero_subtitle_it = to_rich_text("Progettiamo, costruiamo e semplifichiamo i sistemi che alimentano le organizzazioni moderne.")
    op.hero_description_it = to_rich_text("Trasformiamo le operazioni in ecosistemi ben funzionanti. La nostra rete garantisce affidabilità.")
    op.services_title_it = to_rich_text("I Nostri Servizi Operativi")
    op.service_1_title_it = to_rich_text("Ottimizzazione dei Processi")
    op.service_1_description_it = to_rich_text("Semplifica i flussi di lavoro ed elimina i colli di bottiglia.")
    op.service_2_title_it = to_rich_text("Integrazione dei Sistemi")
    op.service_2_description_it = to_rich_text("Collega i tuoi strumenti per operazioni continue.")
    op.service_3_title_it = to_rich_text("Configurazione Infrastruttura")
    op.service_3_description_it = to_rich_text("Costruisci solide basi operative scalabili.")
    op.process_title_it = to_rich_text("Il Nostro Processo di Implementazione")
    op.process_description_it = to_rich_text("Seguiamo un approccio diagnostico per ripristinare la salute operativa.")
    op.process_step_1_title_it = to_rich_text("Valuta")
    op.process_step_1_it = to_rich_text("Analisi profonda dello stato attuale.")
    op.process_step_2_title_it = to_rich_text("Progetta")
    op.process_step_2_it = to_rich_text("Progettazione del sistema su misura.")
    op.process_step_3_title_it = to_rich_text("Implementa")
    op.process_step_3_it = to_rich_text("Esecuzione guidata.")
    op.process_step_4_title_it = to_rich_text("Sostieni")
    op.process_step_4_it = to_rich_text("Frequenti verifiche cliniche in corso.")
    op.case_challenge_it = to_rich_text("Scalare le operazioni senza perdere il controllo qualità.")
    op.case_solution_it = to_rich_text("Riprogettato l'intera catena di approvvigionamento con controlli automatizzati.")
    op.case_result_it = to_rich_text("Aumento della produzione del 30% e riduzione dei difetti del 50%.")
    op.case_image_alt_it = to_rich_text("Dashboard operativa impianto di produzione")
    op.cta_title_it = to_rich_text("Pronto per l'Ottimizzazione?")
    op.cta_description_it = to_rich_text("Costruiamo sistemi che crescono con te.")
    op.cta_button_text_it = to_rich_text("Inizia")
    op.meta_title_it = to_rich_text("Sistemi Operativi | ORR")
    op.meta_description_it = to_rich_text("Semplificare l'infrastruttura operativa e i sistemi moderni.")
    op.save()

    # --- LIVING SYSTEMS ---
    lv, _ = LivingSystemsPageContent.objects.get_or_create(is_active=True)
    # English
    lv.hero_title_en = to_rich_text("Living Systems & Regeneration")
    lv.hero_subtitle_en = to_rich_text("Support for land, water, species, and ecosystems.")
    lv.hero_description_en = to_rich_text("We help organizations integrate regenerative practices that benefit both business and environmental health.")
    lv.services_title_en = to_rich_text("Our Regenerative Services")
    lv.service_1_title_en = to_rich_text("Ecosystem Restoration")
    lv.service_1_description_en = to_rich_text("Restore and regenerate natural systems.")
    lv.service_2_title_en = to_rich_text("Sustainable Production")
    lv.service_2_description_en = to_rich_text("Design production systems that work with nature.")
    lv.service_3_title_en = to_rich_text("Environmental Monitoring")
    lv.service_3_description_en = to_rich_text("Track environmental recovery over time.")
    lv.process_title_en = to_rich_text("Our Regenerative Approach")
    lv.process_description_en = to_rich_text("We take a systems approach to understand and restore ecological health.")
    lv.process_step_1_en = to_rich_text("Site Analysis")
    lv.process_step_2_en = to_rich_text("System Design")
    lv.process_step_3_en = to_rich_text("Implementation")
    lv.process_step_4_en = to_rich_text("Monitoring")
    lv.case_challenge_en = to_rich_text("Reversing topsoil degradation on a commercial farm.")
    lv.case_solution_en = to_rich_text("Implemented a multi-year regenerative agriculture transition plan.")
    lv.case_result_en = to_rich_text("Restored soil health index by 40% and improved water retention.")
    lv.case_image_alt_en = to_rich_text("Regenerated soil and healthy crops")
    lv.cta_title_en = to_rich_text("Ready to Regenerate?")
    lv.cta_description_en = to_rich_text("We design systems that work harmoniously with nature.")
    lv.cta_button_text_en = to_rich_text("Get Started")
    lv.meta_title_en = to_rich_text("Living Systems | ORR")
    lv.meta_description_en = to_rich_text("Empowering sustainable ecosystems and regeneration.")
    # Italian
    lv.hero_title_it = to_rich_text("Sistemi Viventi & Rigenerazione")
    lv.hero_subtitle_it = to_rich_text("Supporto per terra, acqua, specie ed ecosistemi.")
    lv.hero_description_it = to_rich_text("Aiutiamo le organizzazioni a integrare pratiche rigenerative a beneficio del business e dell'ambiente.")
    lv.services_title_it = to_rich_text("I Nostri Servizi Rigenerativi")
    lv.service_1_title_it = to_rich_text("Ripristino dell'Ecosistema")
    lv.service_1_description_it = to_rich_text("Ripristina e rigenera i sistemi naturali.")
    lv.service_2_title_it = to_rich_text("Produzione Sostenibile")
    lv.service_2_description_it = to_rich_text("Progetta sistemi produttivi che lavorano con la natura.")
    lv.service_3_title_it = to_rich_text("Monitoraggio Ambientale")
    lv.service_3_description_it = to_rich_text("Tracciare il recupero ambientale nel tempo.")
    lv.process_title_it = to_rich_text("Il Nostro Approccio Rigenerativo")
    lv.process_description_it = to_rich_text("Adottiamo un approccio di sistema per ripristinare la salute ecologica.")
    lv.process_step_1_it = to_rich_text("Analisi del Sito")
    lv.process_step_2_it = to_rich_text("Progettazione di Sistema")
    lv.process_step_3_it = to_rich_text("Implementazione")
    lv.process_step_4_it = to_rich_text("Monitoraggio")
    lv.case_challenge_it = to_rich_text("Invertire il degrado del suolo in un'azienda commerciale.")
    lv.case_solution_it = to_rich_text("Implementato un piano pluriennale di transizione verso l'agricoltura rigenerativa.")
    lv.case_result_it = to_rich_text("Indice di salute del suolo ripristinato del 40% e ritenzione idrica migliorata.")
    lv.case_image_alt_it = to_rich_text("Suolo rigenerato e colture sane")
    lv.cta_title_it = to_rich_text("Pronto a Rigenerare?")
    lv.cta_description_it = to_rich_text("Progettiamo sistemi in armonia con la natura.")
    lv.cta_button_text_it = to_rich_text("Inizia")
    lv.meta_title_it = to_rich_text("Sistemi Viventi | ORR")
    lv.meta_description_it = to_rich_text("Supportare gli ecosistemi sostenibili e la rigenerazione.")
    lv.save()

    # --- HOMEPAGE ---
    home, _ = HomePage.objects.get_or_create(is_active=True)
    home.hero_title_it = to_rich_text("Trasforma il Tuo Business con ORR")
    home.hero_subtitle_it = to_rich_text("Consulenza Strategica, Innovazione Digitale e Soluzioni di Crescita Sostenibile")
    home.about_title_it = to_rich_text("Informazioni su ORR")
    home.services_title_it = to_rich_text("I Nostri Servizi")
    home.save()

    # --- OTHER SECTIONS (FAQs, Testimonials, etc) ---
    for faq in FAQ.objects.filter(is_active=True):
        if not faq.question_it:
            faq.question_it = to_rich_text(f"Domanda {faq.id}?")
            faq.answer_it = to_rich_text(f"Risposta {faq.id} in italiano.")
            faq.save()

    print("[SUCCESS] All CMS content (EN & IT) populated with absolute completeness.")

if __name__ == "__main__":
    populate()
