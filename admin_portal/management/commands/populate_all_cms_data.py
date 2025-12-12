from django.core.management.base import BaseCommand
from admin_portal.models_cms import (
    HomePage, ServicesPage, ResourcesBlogsPage, LegacyPolicyPage, 
    ContactPage, ApproachSection, BusinessSystemSection, ORRRoleSection,
    MessageStrip, ProcessSection, ORRReportSection, FAQ
)

class Command(BaseCommand):
    help = 'Populate all CMS models with dummy data'

    def handle(self, *args, **options):
        # Homepage
        homepage, created = HomePage.objects.get_or_create(
            is_active=True,
            defaults={
                'hero_title': 'ORR Solutions – Listen. Solve. Optimise.',
                'hero_subtitle': 'Your business GP for complex systems — digital and living.',
                'hero_cta_text': 'Book your free initial consultation',
                'hero_cta_link': '/contact',
                'about_title': 'About ORR',
                'about_content': 'We help organizations navigate complex challenges...',
                'services_title': 'Our Services',
                'services_subtitle': 'Comprehensive solutions for your business',
                'contact_title': 'Get In Touch',
                'contact_subtitle': 'Ready to transform your business?',
                'contact_email': 'info@orr.com',
                'contact_phone': '+1 234 567 8900'
            }
        )

        # Services Page
        services_page, created = ServicesPage.objects.get_or_create(
            is_active=True,
            defaults={
                'hero_title': 'ORR Solutions - Listen. Solve. Optimise.',
                'hero_subtitle': 'We treat your organisation as a whole system — digital, regulatory, and living.',
                'stage_1_title': 'STAGE 1 - DISCOVER',
                'stage_1_subtitle': 'Listen.',
                'stage_1_description': 'We start simple: one calm conversation and a quick scan of your reality.',
                'stage_1_focus': 'We focus on:\n• Your context, people, and pressures\n• Regulatory, operational, data, and environmental risks\n• Which questions actually matter',
                'stage_1_button_text': 'Sign up',
                'stage_2_title': 'STAGE 2 - DIAGNOSE',
                'stage_2_subtitle': 'Think. Then listen again.',
                'stage_2_description': 'We turn symptoms into a clear map of problems and opportunities across three pillars.',
                'stage_2_focus': 'What happens here:\n• Bottleneck and process mapping\n• Compliance, governance, and risk review\n• Data and living systems scan\n• Prioritised list: urgent, high leverage, later',
                'stage_2_button_text': 'Learn More'
            }
        )

        # Resources & Blogs Page
        resources_page, created = ResourcesBlogsPage.objects.get_or_create(
            is_active=True,
            defaults={
                'hero_title': 'Resources / Blogs',
                'hero_subtitle': 'Articles, practical guides, and future-focused insights on digital transformation, AI, software development, and cloud innovation.',
                'blog_card_1_title': 'Mobile Apps & PWAs for Maltese Insurers: Boost Engagement',
                'blog_card_1_category': 'Article',
                'blog_card_1_image': '/images/image.png',
                'admin_tips_title': 'Admin Tips',
                'tip_1_number': '01',
                'tip_1_title': 'Digital Transformation',
                'tip_1_description': 'From regulatory and sustainability frameworks to biotechnology and compliance consulting, our experts guide clients through evolving standards.'
            }
        )

        # Legacy & Policy Page
        legacy_page, created = LegacyPolicyPage.objects.get_or_create(
            is_active=True,
            defaults={
                'hero_title': 'Legacy & Policy',
                'hero_description': 'From regulatory and sustainability frameworks to biotechnology and compliance consulting, our experts guide clients through evolving standards.',
                'policy_item_1_number': '01',
                'policy_item_1_description': 'Regulatory and sustainability frameworks to biotechnology and compliance consulting, ensuring every initiative is compliant and sustainable.',
                'policy_item_2_number': '02',
                'policy_item_2_description': 'Strategic foresight and technical insight combined to navigate complex legal and operational requirements.',
                'policy_item_3_number': '03',
                'policy_item_3_description': 'Built for growth with deep understanding of evolving legal, scientific, and operational standards.'
            }
        )

        # Contact Page
        contact_page, created = ContactPage.objects.get_or_create(
            is_active=True,
            defaults={
                'hero_title': 'Contact Us',
                'contact_info_title': 'Contact Information',
                'contact_info_subtitle': 'Say something to start a live chat!',
                'phone_number': '+012 3456 789',
                'email_address': 'demo@gmail.com',
                'address': '132 Dartmouth Street Boston, Massachusetts 02156 United States',
                'submit_button_text': 'Send Message'
            }
        )

        # Approach Section
        approach_section, created = ApproachSection.objects.get_or_create(
            is_active=True,
            defaults={
                'title': 'Supporting Copy',
                'paragraph_1': 'Just like a skilled general practitioner, we start from your story not our framework.',
                'paragraph_2': 'We\'re not a lone consultant — we\'re a central coordination layer with a distributed network behind it.',
                'paragraph_3': 'We fix what\'s slowing you down, strengthen systems around how your people actually work.'
            }
        )

        # Business System Section
        business_system_section, created = BusinessSystemSection.objects.get_or_create(
            is_active=True,
            defaults={
                'title': 'Businesses as a Living System',
                'subtitle': 'Think of your organisation like a body',
                'card_1_title': 'Nervous System',
                'card_1_description': 'Communication, data flow, and decision-making pathways',
                'card_2_title': 'Circulatory System',
                'card_2_description': 'Cash flow, resource distribution, and value exchange',
                'card_3_title': 'Immune System',
                'card_3_description': 'Risk management, compliance, and protective measures'
            }
        )

        # ORR Role Section
        orr_role_section, created = ORRRoleSection.objects.get_or_create(
            is_active=True,
            defaults={
                'title': 'ORR\'s Role',
                'description': 'We act like specialist doctors for your business physiology - but we start from your symptoms and your priorities.'
            }
        )

        # Message Strip
        message_strip, created = MessageStrip.objects.get_or_create(
            is_active=True,
            defaults={
                'title': 'Message Strip',
                'message': 'Businesses thrive like living organisms when all their systems work together around real human needs.',
                'user_image_1': '/images/user-1.jpg',
                'user_image_2': '/images/user-2.jpg',
                'user_image_3': '/images/user-3.jpg',
                'user_image_4': '/images/user-4.jpg'
            }
        )

        # Process Section
        process_section, created = ProcessSection.objects.get_or_create(
            is_active=True,
            defaults={
                'title': 'How we work: Five Stages',
                'subtitle': 'Every stage is built around you – your pace, your risk appetite, your resources',
                'stage_1_title': 'Discover - We listen',
                'stage_1_description': 'You tell us what\'s happening. We map your context, pressures, and goals.',
                'stage_2_title': 'Diagnose - We find root causes',
                'stage_2_description': 'SOPs, workflows, portals, dashboards, and AI-assisted tools designed around your team.',
                'stage_3_title': 'Design - We shape solution with you',
                'stage_3_description': 'We propose clear, actionable structures that fit your reality.',
                'stage_4_title': 'Deploy - We put them to work together',
                'stage_4_description': 'We implement with minimal disruption, adapting to how your people work.',
                'stage_5_title': 'Grow - We optimise over time',
                'stage_5_description': 'We monitor, refine, and help you scale intelligently.'
            }
        )

        # ORR Report Section
        orr_report_section, created = ORRReportSection.objects.get_or_create(
            is_active=True,
            defaults={
                'title': 'What you Get: The ORR Report',
                'subtitle': 'After your first meeting, you receive a decision-ready ORR report designed to be immediately useful.',
                'feature_1': 'explain your situation in your language,',
                'feature_2': 'highlights key issues and risks that affect your customers and teams',
                'feature_3': 'proposes quick fixes and longer-term improvements that respect your constraints',
                'feature_4': 'shows where advisory, digital systems/AI, or living-systems work will have most impact'
            }
        )

        # FAQs
        faqs_data = [
            {
                'question': 'What makes ORR different from other consultants?',
                'answer': 'We act as your business GP, starting from your story rather than our framework. We provide a central coordination layer with a distributed network of specialists.',
                'category': 'general',
                'order': 1
            },
            {
                'question': 'How long does the typical engagement take?',
                'answer': 'Every engagement is built around your pace, risk appetite, and resources. We work through five stages from discovery to growth optimization.',
                'category': 'process',
                'order': 2
            },
            {
                'question': 'What industries do you work with?',
                'answer': 'We work across industries, focusing on digital systems, regulatory compliance, and living systems regardless of sector.',
                'category': 'services',
                'order': 3
            }
        ]

        for faq_data in faqs_data:
            FAQ.objects.get_or_create(
                question=faq_data['question'],
                defaults=faq_data
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated all CMS data'))