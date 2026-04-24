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
    print("Populating ALL CMS content with comprehensive data...")

    # 1. Strategic Advisory
    strategic, _ = StrategicAdvisoryPageContent.objects.get_or_create(is_active=True)
    strategic.hero_title_en = to_rich_text("Strategic Advisory & Compliance")
    strategic.hero_subtitle_en = to_rich_text("We deliver clarity to complexity. Our experts guide clients through evolving landscapes.")
    strategic.service_2_title_en = to_rich_text("ESG & Sustainability Strategy")
    strategic.service_2_description_en = to_rich_text("Build sustainable business practices that drive long-term value.")
    strategic.service_3_title_en = to_rich_text("Corporate Risk Management")
    strategic.service_3_description_en = to_rich_text("Identify and mitigate business risks proactively.")
    strategic.process_title_en = to_rich_text("Our Strategic Process")
    strategic.process_subtitle_en = to_rich_text("Listen . Solve . Optimize")
    strategic.process_description_en = to_rich_text("Like your Business GP, we diagnose compliance challenges and prescribe solutions.")
    strategic.network_title_en = to_rich_text("The ORR Network Advantage")
    strategic.network_description_en = to_rich_text("Complex challenges require diverse expertise. We activate global specialists.")
    strategic.digital_title_en = to_rich_text("Digital Solutions for")
    strategic.digital_subtitle_en = to_rich_text("Compliance Management")
    strategic.save()

    # 2. FAQs
    if not FAQ.objects.exists():
        FAQ.objects.create(
            question_en=to_rich_text("What happens in the first meeting?"),
            answer_en=to_rich_text("We listen first to understand your context and constraints."),
            category='general',
            order=1
        )
    
    # 3. Testimonials
    if not Testimonial.objects.exists():
        Testimonial.objects.create(
            client_name_en=to_rich_text("Sarah Jenkins"),
            testimonial_text_en=to_rich_text("ORR transformed our approach to compliance."),
            client_role_en=to_rich_text("CTO, Biotech Innovate"),
            order=1
        )

    # 4. Business System Section
    bss, _ = BusinessSystemSection.objects.get_or_create(is_active=True)
    bss.title_en = to_rich_text("Organisation as a Living System")
    bss.subtitle_en = to_rich_text("Thinking of your business like a human body.")
    bss.card_1_title_en = to_rich_text("Nervous System")
    bss.card_1_description_en = to_rich_text("Communication and data flow.")
    bss.save()

    print("[SUCCESS] Comprehensive CMS population complete.")

if __name__ == "__main__":
    populate()
