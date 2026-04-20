#!/usr/bin/env python
import os
import sys
import django
from django.conf import settings

# 1. Get the password from environment
db_pass = os.environ.get('DB_PASS')
if not db_pass:
    print("Error: DB_PASS environment variable not set.")
    sys.exit(1)

# 2. Configure Django settings MANUALLY to bypass production.py issues
if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'my_production_db',
                'USER': 'postgres',
                'PASSWORD': db_pass,
                'HOST': '34.134.52.218',
                'PORT': '5432',
                'OPTIONS': {
                    'sslmode': 'require',
                }
            }
        },
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.auth',
            'admin_portal', # This is where your CMS models live
        ],
        TIME_ZONE='UTC',
        USE_TZ=True,
    )
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
    homepage = HomePage.objects.all().first()
    if homepage:
        homepage.hero_title_it = "Trasforma il tuo Business con ORR"
        homepage.hero_subtitle_it = "Consulenza Strategica, Innovazione Digitale e Soluzioni di Crescita Sostenibile"
        homepage.hero_cta_text_it = "Inizia Ora"
        homepage.about_title_it = "Chi è ORR"
        homepage.about_content_it = "Aiutiamo le organizzazioni a navigare sfide complesse..."
        homepage.services_title_it = "I Nostri Servizi"
        homepage.save()
        print("[OK] Homepage Italian translations updated")

    # 2. Approach Section
    approach = ApproachSection.objects.all().first()
    if approach:
        approach.title_it = "L'Approccio ORR"
        approach.paragraph_1_it = "Proprio come un medico di base esperto, partiamo dalla vostra storia, non dal nostro framework."
        approach.paragraph_2_it = "Non siamo un consulente solitario — siamo un livello di coordinamento centrale."
        approach.paragraph_3_it = "Sistemiamo ciò che vi rallenta, rafforziamo i sistemi."
        approach.save()
        print("[OK] Approach Section updated")

    # 3. Business System Section
    biz_sys = BusinessSystemSection.objects.all().first()
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
