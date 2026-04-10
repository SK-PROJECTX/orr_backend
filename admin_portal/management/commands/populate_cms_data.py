from django.core.management.base import BaseCommand
from admin_portal.models_cms import (
    HomePage, FAQ, ApproachSection, BusinessSystemSection, 
    ORRRoleSection, MessageStrip, ProcessSection, ORRReportSection,
    ContactInfo
)


class Command(BaseCommand):
    help = 'Populate initial CMS data'

    def handle(self, *args, **options):
        self.stdout.write('Populating CMS data...')

        # Create or update HomePage
        homepage, created = HomePage.objects.get_or_create(
            is_active=True,
            defaults={
                'hero_title': 'ORR Solutions – Listen. Solve. Optimise.',
                'hero_subtitle': 'Your business GP for complex systems — digital and living.',
                'hero_cta_text': 'Book your free initial consultation',
                'services_title': 'Our Three Pillars',
                'service_1_title': 'Strategic Advisory & Compliance',
                'service_1_description': 'Navigate complex regulations and strategic decisions with expert guidance tailored to your industry and context.',
                'service_1_button': 'Learn More',
                'service_2_title': 'Digital Systems, Automation & AI',
                'service_2_description': 'Streamline operations with intelligent automation and AI solutions that work with your existing processes.',
                'service_2_button': 'Explore Solutions',
                'service_3_title': 'Living Systems & Regeneration',
                'service_3_description': 'Build sustainable, regenerative business practices that benefit both your organization and the environment.',
                'service_3_button': 'Get Started',
            }
        )
        if created:
            self.stdout.write(f'Created homepage: {homepage}')
        else:
            self.stdout.write(f'Homepage already exists: {homepage}')

        # Create FAQs
        faqs_data = [
            {
                'question': 'What does it mean that ORR is a business GP?',
                'answer': 'We work like a general practitioner for your organisation. We listen first, understand your context and constraints, then bring in the right mix of advisory, systems, AI, and nature-related expertise to treat root causes — always anchored in what matters most to you and your customers.',
                'category': 'general',
                'order': 1
            },
            {
                'question': 'What happens in the first meeting?',
                'answer': 'In our first meeting, we focus on understanding your current situation, challenges, and goals. We\'ll discuss your business context, identify key pain points, and explore what success looks like for you. This helps us create a tailored ORR report with actionable recommendations.',
                'category': 'process',
                'order': 2
            },
            {
                'question': 'What is the ORR report?',
                'answer': 'The ORR report is a comprehensive analysis we provide after our first meeting. It outlines key issues affecting your business, proposes quick fixes and long-term improvements, and shows where our advisory, digital systems, or living systems work will have the most impact on your organization.',
                'category': 'services',
                'order': 3
            },
            {
                'question': 'How much do the meetings and report cost?',
                'answer': 'Our meetings are charged at €45/hour on a pro-rata basis, designed to be short, focused, and value-dense. The ORR report fee starts at €220, though the final cost depends on the complexity of your situation and requirements.',
                'category': 'pricing',
                'order': 4
            },
            {
                'question': 'Do I have to keep working with ORR after the report?',
                'answer': 'Not at all. The ORR report is designed to provide value whether you continue working with us or not. It includes actionable recommendations you can implement independently. However, we\'re available to support implementation if you choose to continue our partnership.',
                'category': 'general',
                'order': 5
            }
        ]

        for faq_data in faqs_data:
            faq, created = FAQ.objects.get_or_create(
                question=faq_data['question'],
                defaults=faq_data
            )
            if created:
                self.stdout.write(f'Created FAQ: {faq.question}')
            else:
                self.stdout.write(f'FAQ already exists: {faq.question}')

        # Create other sections
        approach, created = ApproachSection.objects.get_or_create(is_active=True)
        if created:
            self.stdout.write(f'Created approach section: {approach}')

        business_system, created = BusinessSystemSection.objects.get_or_create(is_active=True)
        if created:
            self.stdout.write(f'Created business system section: {business_system}')

        orr_role, created = ORRRoleSection.objects.get_or_create(is_active=True)
        if created:
            self.stdout.write(f'Created ORR role section: {orr_role}')

        message_strip, created = MessageStrip.objects.get_or_create(is_active=True)
        if created:
            self.stdout.write(f'Created message strip: {message_strip}')

        process_section, created = ProcessSection.objects.get_or_create(is_active=True)
        if created:
            self.stdout.write(f'Created process section: {process_section}')

        orr_report, created = ORRReportSection.objects.get_or_create(is_active=True)
        if created:
            self.stdout.write(f'Created ORR report section: {orr_report}')

        contact_info, created = ContactInfo.objects.get_or_create(
            is_active=True,
            defaults={
                'company_name': 'ORR',
                'email': 'info@orr.com'
            }
        )
        if created:
            self.stdout.write(f'Created contact info: {contact_info}')

        self.stdout.write(self.style.SUCCESS('Successfully populated CMS data!'))