#!/usr/bin/env python
"""
Utility script to update Italian translations for CMS content in the PRODUCTION database.
Usage: 
1. Set DATABASE_URL environment variable to your production DB.
2. Run: python sync_production_translations.py
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.production')
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
    print("Updating Italian translations for PRODUCTION CMS content...")

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

    # 3. Process Steps
    steps_it = {
        '01': {'title': "L'Inizio",'bullet1': 'Una conversazione tranquilla.','bullet2': 'Un problema.','bullet3': 'Un punto di pressione.','bullet4': 'Una storia che finalmente viene raccontata.',},
        '02': {'title': 'La Prima Mappa','subtitle': "Dopo l'incontro, il rumore si schiarisce.",'description': "Apriamo una pagina bianca e iniziamo a disegnare la prima mappa della vostra organizzazione."},
        '05': {'title': 'Il Rapporto ORR','subtitle': 'Raggiungete il punto decisionale.','description': 'Ciò che ricevete non è decorazione — ma un modello strutturato:'}
    }
    for step_num, trans in steps_it.items():
        step = ProcessStep.objects.filter(step_number=step_num).first()
        if step:
            for field, value in trans.items():
                setattr(step, f"{field}_it", value)
            step.save()
            print(f"[OK] Process Step {step_num} updated")

    # 4. Approach Section
    approach = ApproachSection.objects.filter(is_active=True).first()
    if approach:
        approach.title_it = "L'Approccio ORR"
        approach.paragraph_1_it = "Proprio come un medico di base esperto, partiamo dalla vostra storia, non dal nostro framework."
        approach.paragraph_2_it = "Non siamo un consulente solitario — siamo un livello di coordinamento centrale."
        approach.paragraph_3_it = "Sistemiamo ciò che vi rallenta, rafforziamo i sistemi."
        approach.save()
        print("[OK] Approach Section updated")

    # 5. Business System Section
    biz_sys = BusinessSystemSection.objects.filter(is_active=True).first()
    if biz_sys:
        biz_sys.title_it = "L'Azienda come Sistema Vivente"
        biz_sys.card_1_title_it = "Sistema Nervoso"
        biz_sys.card_2_title_it = "Sistema Circolatorio"
        biz_sys.card_3_title_it = "Sistema Immunitario"
        biz_sys.save()
        print("[OK] Business System Section updated")

    print("\nTranslation update complete for production!")

if __name__ == '__main__':
    update_translations()
