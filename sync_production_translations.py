#!/usr/bin/env python
import os
import sys
import django
import json
from django.conf import settings
from django.db import connection

# 1. Get the password from environment
db_pass = os.environ.get('DB_PASS')
if not db_pass:
    print("Error: DB_PASS environment variable not set.")
    sys.exit(1)

# 2. Configure Django settings MANUALLY
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
            'admin_portal', 
        ],
        TIME_ZONE='UTC',
        USE_TZ=True,
    )
    django.setup()

from admin_portal.models_cms import HomePage, ApproachSection

def to_jsonb(text):
    """Convert plain text to the JSON structure expected by the CMS RichTextField"""
    return json.dumps({"content": str(text), "format": "html"})

def update_translations():
    print("Updating translations for PRODUCTION CMS content...")
    
    with connection.cursor() as cursor:
        # 1. Homepage
        homepage = HomePage.objects.all().first()
        if homepage:
            print(f"Updating Homepage (ID: {homepage.id})...")
            # Ensure columns exist (both _en and _it)
            for col in ['hero_title', 'hero_subtitle', 'hero_cta_text', 'about_title', 'about_content', 'services_title']:
                cursor.execute(f"ALTER TABLE admin_portal_homepage ADD COLUMN IF NOT EXISTS {col}_en jsonb;")
                cursor.execute(f"ALTER TABLE admin_portal_homepage ADD COLUMN IF NOT EXISTS {col}_it jsonb;")
            
            # Update values
            cursor.execute("""
                UPDATE admin_portal_homepage 
                SET hero_title_en = %s, hero_title_it = %s,
                    hero_subtitle_en = %s, hero_subtitle_it = %s,
                    hero_cta_text_en = %s, hero_cta_text_it = %s,
                    about_title_en = %s, about_title_it = %s,
                    about_content_en = %s, about_content_it = %s,
                    services_title_en = %s, services_title_it = %s
                WHERE id = %s
            """, [
                to_jsonb(homepage.hero_title), to_jsonb("Trasforma il tuo Business con ORR"),
                to_jsonb(homepage.hero_subtitle), to_jsonb("Consulenza Strategica, Innovazione Digitale e Soluzioni di Crescita Sostenibile"),
                to_jsonb(homepage.hero_cta_text), to_jsonb("Inizia Ora"),
                to_jsonb(homepage.about_title), to_jsonb("Chi è ORR"),
                to_jsonb(homepage.about_content), to_jsonb("Aiutiamo le organizzazioni a navigare sfide complesse..."),
                to_jsonb(homepage.services_title), to_jsonb("I Nostri Servizi"),
                homepage.id
            ])
            print("[OK] Homepage updated")

        # 2. Approach Section (The "Supporting Copy" reported by user)
        approach = ApproachSection.objects.all().first()
        if approach:
            print(f"Updating Approach Section (ID: {approach.id})...")
            for col in ['title', 'paragraph_1', 'paragraph_2', 'paragraph_3']:
                cursor.execute(f"ALTER TABLE admin_portal_approachsection ADD COLUMN IF NOT EXISTS {col}_en jsonb;")
                cursor.execute(f"ALTER TABLE admin_portal_approachsection ADD COLUMN IF NOT EXISTS {col}_it jsonb;")
            
            cursor.execute("""
                UPDATE admin_portal_approachsection
                SET title_en = %s, title_it = %s,
                    paragraph_1_en = %s, paragraph_1_it = %s,
                    paragraph_2_en = %s, paragraph_2_it = %s,
                    paragraph_3_en = %s, paragraph_3_it = %s
                WHERE id = %s
            """, [
                to_jsonb(approach.title), to_jsonb("L'Approccio ORR"),
                to_jsonb(approach.paragraph_1), to_jsonb("Proprio come un medico di base esperto, partiamo dalla vostra storia, non dal nostro framework. Ci prendiamo il tempo per capire come funziona davvero la vostra azienda prima di prescrivere qualsiasi cosa."),
                to_jsonb(approach.paragraph_2), to_jsonb("Non siamo un consulente solitario — siamo un livello di coordinamento centrale con una rete distribuita alle spalle. Quando necessario, attingiamo a specialisti in tutti i continenti, ma avrete sempre un unico punto di contatto: ORR, focalizzato su ciò che è meglio per voi."),
                to_jsonb(approach.paragraph_3), to_jsonb("Sistemiamo ciò che vi rallenta, rafforziamo i sistemi in base a come lavorano effettivamente le vostre persone e, quando è necessario un contributo più approfondito, lo introduciamo al momento giusto — sempre al servizio dei vostri obiettivi."),
                approach.id
            ])
            print("[OK] Approach Section updated")

    print("\nTranslation update complete for production!")

if __name__ == '__main__':
    update_translations()
