#!/usr/bin/env python
"""
Utility script to update Italian and Arabic translations for CMS content in the database.
Includes full content for Living Systems, Strategic Advisory, and Operational Systems.
"""
import os
import sys
import django
import json

# Add properties for production connection if --prod flag is present
if "--prod" in sys.argv:
    print("RUNNING IN PRODUCTION MODE...")
    from django.conf import settings
    if not settings.configured:
        settings.configure(
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.postgresql',
                    'NAME': 'my_production_db',
                    'USER': 'app_user',
                    'PASSWORD': 'Ojugbele2006#',
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
                'rest_framework',
                'modeltranslation',
            ],
            MODELTRANSLATION_DEFAULT_LANGUAGE='en',
            MODELTRANSLATION_LANGUAGES=('en', 'it', 'ar'),
            SECRET_KEY='prod-sync-key',
        )
        django.setup()
else:
    # Add the project directory to the Python path
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    # Set up Django (Development)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.development')
    django.setup()

from admin_portal.models_cms import (
    StrategicAdvisoryPageContent,
    OperationalSystemsPageContent,
    LivingSystemsPageContent
)

def to_rich_text(text):
    return {"format": "html", "content": str(text)}

def update_living_systems():
    print("Updating Living Systems content & translations...")
    obj, created = LivingSystemsPageContent.objects.get_or_create(id=1)

    # English
    obj.hero_title_en = to_rich_text("Living Systems & Regenerations")
    obj.hero_subtitle_en = to_rich_text("We work with living systems — landscapes, forests, oceans, and ecosystems — to design regenerative solutions that bring life back to degraded environments.")
    obj.hero_description_en = to_rich_text("From farms and urban plots to coastlines, regenerative agriculture and circular economy design, we help organizations create systems that restore biodiversity, sequester carbon, and build resilience. Whether you're enhancing a living farm functionality, planning a restoration project, or designing regenerative infrastructure, we provide the expertise to create systems that regenerate rather than extract.")
    
    obj.services_title_en = to_rich_text("What We Offer")
    obj.service_1_title_en = to_rich_text("Regenerative Agriculture & Bio Systems")
    obj.service_1_description_en = to_rich_text("Transform agricultural practices to restore soil health, enhance biodiversity, and create resilient food systems.")
    obj.service_2_title_en = to_rich_text("Regenerative Land Economy Design")
    obj.service_2_description_en = to_rich_text("Design business models and systems that eliminate waste and regenerate natural systems through circular principles.")
    obj.service_3_title_en = to_rich_text("Wetland, Rangeland & Forest Restoration")
    obj.service_3_description_en = to_rich_text("Restore degraded ecosystems and implement conservation strategies that enhance biodiversity.")
    
    obj.process_title_en = to_rich_text("Our Regenerative Approach")
    obj.process_description_en = to_rich_text("We follow a systematic process to ensure ecological restoration and long-term sustainability.")
    obj.process_step_1_en = to_rich_text("We begin with comprehensive site assessment and system analysis to understand current ecological conditions, resource flows, and regenerative potential.")
    obj.process_step_2_en = to_rich_text("Once you receive the regeneration report, you choose your path forward: Use the report independently to guide internal regeneration efforts or engage ORR for ongoing implementation support through tailored partnership.")
    obj.process_step_3_en = to_rich_text("For ongoing partnerships, we move into implementation and stewardship phases. We execute regenerative solutions, build ecological infrastructure, and establish monitoring systems.")
    obj.process_step_4_en = to_rich_text("Systems need to evolve with nature. We provide ongoing support and refinement.")

    obj.case_challenge_en = to_rich_text("A large agricultural cooperative was facing declining soil health, reduced biodiversity, and increasing input costs from conventional farming practices.")
    obj.case_solution_en = to_rich_text("ORR conducted a comprehensive ecological assessment and delivered a detailed regeneration report outlining soil restoration strategies.")
    obj.case_result_en = to_rich_text("The cooperative increased organic matter by 40% and decreased input costs by 30% within two years.")
    obj.case_image_alt_en = "Regenerative agriculture landscape showing restored soil and biodiversity"
    
    obj.cta_title_en = to_rich_text("Ready to Work With Your Living Systems, Not Against Them?")
    obj.cta_description_en = to_rich_text("Let's help your business discover and design systems that regenerate rather than deplete.")
    obj.cta_button_text_en = "Book a free Living Systems assessment"

    # Italian
    obj.hero_title_it = to_rich_text("Sistemi Viventi & Rigenerazione")
    obj.hero_subtitle_it = to_rich_text("Lavoriamo con i sistemi viventi — paesaggi, foreste, oceani ed ecosistemi — per progettare soluzioni rigenerative che riportino la vita negli ambienti degradati.")
    obj.hero_description_it = to_rich_text("Dalle fattorie e appezzamenti urbani alle coste, dall'agricoltura rigenerativa al design dell'economia circolare, aiutiamo le organizzazioni a creare sistemi che ripristinano la biodiversità, sequestrano il carbonio e costruiscono resilienza.")
    
    obj.services_title_it = to_rich_text("Cosa Offriamo")
    obj.service_1_title_it = to_rich_text("Agricoltura Rigenerativa & Bio Sistemi")
    obj.service_1_description_it = to_rich_text("Trasformare le pratiche agricole per ripristinare la salute del suolo, migliorare la biodiversità e creare sistemi alimentari resilienti.")
    obj.service_2_title_it = to_rich_text("Design dell'Economia Territoriale Rigenerativa")
    obj.service_2_description_it = to_rich_text("Progettare modelli di business e sistemi che eliminano gli sprechi e rigenerano i sistemi naturali attraverso principi circolari.")
    obj.service_3_title_it = to_rich_text("Ripristino di Zone Umide, Pascoli e Foreste")
    obj.service_3_description_it = to_rich_text("Ripristinare gli ecosistemi degradati e implementare strategie di conservazione.")
    
    obj.process_title_it = to_rich_text("Nostro Approccio Rigenerativo")
    obj.process_description_it = to_rich_text("Seguiamo un processo sistematico per garantire il ripristino ecologico e la sostenibilità a lungo termine.")
    obj.process_step_1_it = to_rich_text("Iniziamo con una valutazione completa del sito e un'analisi del sistema per comprendere le condizioni ecologiche attuali.")
    obj.process_step_2_it = to_rich_text("Una volta ricevuto il rapporto, scegliete il vostro percorso: utilizzate il rapporto in autonomia o collaborate con ORR per il supporto all'attuazione.")
    obj.process_step_3_it = to_rich_text("Per le partnership continuative, passiamo alle fasi di attuazione e gestione responsabile.")

    obj.case_challenge_it = to_rich_text("Una grande cooperativa agricola stava affrontando il declino della salute del suolo e la riduzione della biodiversità.")
    obj.case_solution_it = to_rich_text("ORR ha condotto una valutazione ecologica completa e ha consegnato un rapporto di rigenerazione dettagliato.")
    obj.case_result_it = to_rich_text("La cooperativa ha aumentato la materia organica del 40% e ha ridotto i costi dei fattori produttivi del 30% in due anni.")
    obj.case_image_alt_it = "Paesaggio di agricoltura rigenerativa che mostra suolo ripristinato"
    
    obj.cta_title_it = to_rich_text("Pronto a lavorare con i tuoi sistemi viventi, non contro di loro?")
    obj.cta_description_it = to_rich_text("Aiutiamo la tua azienda a scoprire e progettare sistemi che rigenerano invece di esaurire.")
    obj.cta_button_text_it = "Prenota una valutazione gratuita"

    # Arabic
    obj.hero_title_ar = to_rich_text("الأنظمة الحية والتجديد")
    obj.hero_subtitle_ar = to_rich_text("نحن نعمل مع الأنظمة الحية - المناظر الطبيعية والغابات والمحيطات والأنظمة البيئية - لتصميم حلول تجديدية.")
    obj.hero_description_ar = to_rich_text("من المزارع والمخططات الحضرية إلى السواحل، نساعد المؤسسات على إنشاء أنظمة تستعيد التنوع البيولوجي.")
    
    obj.services_title_ar = to_rich_text("ماذا نقدم")
    obj.service_1_title_ar = to_rich_text("الزراعة المتجددة والأنظمة الحيوية")
    obj.service_1_description_ar = to_rich_text("تحويل الممارسات الزراعية لاستعادة صحة التربة وتعزيز التنوع البيولوجي.")
    obj.service_2_title_ar = to_rich_text("تصميم اقتصاد الأراضي المتجدد")
    obj.service_2_description_ar = to_rich_text("تصميم نماذج أعمال تقضي على الهدر وتجدد الأنظمة الطبيعية.")
    obj.service_3_title_ar = to_rich_text("ترميم الأراضي الرطبة والغابات")
    obj.service_3_description_ar = to_rich_text("استعادة الأنظمة البيئية المتدهورة وتنفيذ استراتيجيات الحفظ.")
    
    obj.process_title_ar = to_rich_text("نهجنا التجديدي")
    obj.process_description_ar = to_rich_text("نتبع عملية منهجية لضمان الاستعادة البيئية والاستدامة طويلة الأمد.")
    obj.process_step_1_ar = to_rich_text("نبدأ بتقييم شامل للموقع وتحليل النظام لفهم الظروف البيئية الحالية.")
    obj.process_step_2_ar = to_rich_text("بمجرد استلام التقرير، تختار طريقك للمضي قدماً: استخدم التقرير بشكل مستقل أو استعن بـ ORR للدعم.")

    obj.case_challenge_ar = to_rich_text("كانت تعاونية زراعية كبيرة تواجه تدهور صحة التربة وانخفاض التنوع البيولوجي.")
    obj.case_solution_ar = to_rich_text("أجرت ORR تقييماً بيئياً شاملاً وقدمت تقريراً مفصلاً عن التجديد.")
    obj.case_result_ar = to_rich_text("زادت التعاونية المادة العضوية بنسبة 40٪ وخفضت تكاليف المدخلات بنسبة 30٪ في غضون عامين.")
    obj.case_image_alt_ar = "مناظر طبيعية للزراعة المتجددة تظهر التربة المستعادة"
    
    obj.cta_title_ar = to_rich_text("هل أنت مستعد للعمل مع أنظمتك الحية؟")
    obj.cta_description_ar = to_rich_text("لنساعد عملك على اكتشاف وتصميم أنظمة تجدد بدلاً من استنزافها.")
    obj.cta_button_text_ar = "احجز تقييماً مجانياً"

    obj.save()
    print("[SUCCESS] Living Systems content populated.")

def update_operational_systems():
    print("Updating Operational Systems content & translations...")
    obj, created = OperationalSystemsPageContent.objects.get_or_create(id=1)
    
    # English
    obj.hero_title_en = to_rich_text("Operational Systems & Infrastructure")
    obj.hero_subtitle_en = to_rich_text("We design, build and streamline the systems that power modern organizations.")
    obj.hero_description_en = to_rich_text("We turn operations into well-functioning ecosystems. Our trusted network delivers reliability from planning to execution.")
    
    obj.services_title_en = to_rich_text("Our Operational Services")
    obj.service_1_title_en = to_rich_text("Process Optimization")
    obj.service_1_description_en = to_rich_text("Streamline workflows and eliminate operational bottlenecks.")
    obj.service_2_title_en = to_rich_text("System Integration")
    obj.service_2_description_en = to_rich_text("Connect your tools and platforms for seamless operations.")
    obj.service_3_title_en = to_rich_text("Infrastructure Setup")
    obj.service_3_description_en = to_rich_text("Build robust operational foundations that scale.")
    
    obj.process_title_en = to_rich_text("Our Implementation Process")
    obj.process_description_en = to_rich_text("We start by listening and then prescribe tailored solutions.")
    obj.process_step_1_en = to_rich_text("We start by listening — understanding your current systems and goals.")
    obj.process_step_2_en = to_rich_text("Based on our assessment, we prescribe tailored solutions built for your context.")
    obj.process_step_3_en = to_rich_text("Systems need to evolve. We provide ongoing support.")
    
    obj.case_challenge_en = to_rich_text("A growing tech startup was drowning in manual processes and disconnected tools.")
    obj.case_solution_en = to_rich_text("ORR streamlined their workflows and integrated their core platforms.")
    obj.case_result_en = to_rich_text("The startup saved 20 hours per week of manual labor.")
    
    obj.cta_title_en = to_rich_text("Ready to Build Better Systems?")
    obj.cta_button_text_en = "Book a free assessment"

    # Italian
    obj.hero_title_it = to_rich_text("Sistemi Operativi & Infrastrutture")
    obj.hero_subtitle_it = to_rich_text("Progettiamo, costruiamo e ottimizziamo i sistemi che alimentano le organizzazioni moderne.")
    
    # Arabic
    obj.hero_title_ar = to_rich_text("الأنظمة التشغيلية والبنية التحتية")
    obj.hero_subtitle_ar = to_rich_text("نحن نصمم ونبني ونبسط الأنظمة التي تدعم المؤسسات الحديثة.")

    obj.save()
    print("[SUCCESS] Operational Systems updated.")

def update_strategic_advisory():
    print("Updating Strategic Advisory content & translations...")
    obj, created = StrategicAdvisoryPageContent.objects.get_or_create(id=1)
    
    # English
    obj.hero_title_en = to_rich_text("Strategic Advisory & Compliance")
    obj.hero_subtitle_en = to_rich_text("We deliver clarity to complexity. Our experts guide clients through evolving landscapes.")
    
    obj.services_title_en = to_rich_text("Our Strategic Services")
    obj.service_1_title_en = to_rich_text("Regulatory Compliance & Advisory")
    obj.service_1_description_en = to_rich_text("Navigate complex regulatory landscapes with confidence.")
    
    # Italian
    obj.hero_title_it = to_rich_text("Consulenza Strategica & Compliance")
    obj.hero_subtitle_it = to_rich_text("Portiamo chiarezza nella complessità.")
    
    # Arabic
    obj.hero_title_ar = to_rich_text("الاستشارات الاستراتيجية والامتثال")
    obj.hero_subtitle_ar = to_rich_text("نحن نقدم الوضوح للتعقيد.")

    obj.save()
    print("[SUCCESS] Strategic Advisory updated.")

if __name__ == '__main__':
    update_living_systems()
    update_operational_systems()
    update_strategic_advisory()
