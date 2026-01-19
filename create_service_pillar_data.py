#!/usr/bin/env python
"""
Script to create service pillar page content in the database
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.staging')
django.setup()

from admin_portal.models_cms import (
    StrategicAdvisoryPageContent, 
    OperationalSystemsPageContent, 
    LivingSystemsPageContent
)

def create_service_pillar_content():
    """Create or update service pillar page content"""
    
    print("Creating/updating service pillar page content...")
    
    # Strategic Advisory Page
    strategic_advisory, created = StrategicAdvisoryPageContent.objects.update_or_create(
        is_active=True,
        defaults={
            'hero_title': 'Strategic Advisory & Compliance',
            'hero_subtitle': 'We deliver clarity to complexity. From regulatory and sustainability frameworks to biotechnology and compliance consulting, our experts guide clients through evolving landscapes with confidence.',
            'hero_description': 'Our approach combines deep technical insight with strategic foresight, ensuring every initiative is compliant, sustainable, and built for growth.',
            'services_title': 'Our Strategic Services',
            'service_1_title': 'Regulatory Compliance & Advisory',
            'service_1_description': 'Navigate complex regulatory landscapes with confidence. We provide strategic guidance on compliance requirements, regulatory changes, and implementation strategies.',
            'service_2_title': 'ESG & Sustainability Strategy',
            'service_2_description': 'Develop comprehensive ESG frameworks that meet stakeholder expectations while driving business value. From carbon accounting to sustainability reporting.',
            'service_3_title': 'Biotechnology & Life Sciences Consulting',
            'service_3_description': 'Leverage our network of scientific experts to navigate the technical and regulatory complexities of biotechnology and life sciences.',
            'process_title': 'Our Strategic Process',
            'process_step_1': 'We start with a focused initial meeting to understand your compliance challenges, regulatory environment, and strategic objectives.',
            'process_step_2': 'Once you receive the report, you choose your path forward: Use the report independently or engage ORR for ongoing implementation support.',
            'process_step_3': 'For clients who choose ongoing partnership, we move into implementation and optimization.',
            'cta_title': 'Ready to Navigate Complexity with Confidence?',
            'cta_description': "Let's assess your compliance landscape and design strategies that protect and enable your growth.",
            'cta_button_text': 'Book a free compliance assessment'
        }
    )
    
    if created:
        print("Created Strategic Advisory page content")
    else:
        print("Strategic Advisory page content already exists")
    
    # Operational Systems Page
    operational_systems, created = OperationalSystemsPageContent.objects.update_or_create(
        is_active=True,
        defaults={
            'hero_title': 'Operational Systems & Infrastructure',
            'hero_subtitle': 'We design, build and streamline the systems that power modern organizations. Whether it\'s creating SOPs, structuring workflows, or coordinating complex setups.',
            'hero_description': 'We turn operations into well-functioning ecosystems. Our trusted network of builders and tech specialists delivers reliability from planning to execution.',
            'services_title': 'Our Operational Services',
            'service_1_title': 'Process Optimization',
            'service_1_description': 'Streamline workflows and eliminate operational bottlenecks',
            'service_2_title': 'System Integration',
            'service_2_description': 'Connect your tools and platforms for seamless operations',
            'service_3_title': 'Infrastructure Setup',
            'service_3_description': 'Build robust operational foundations that scale',
            'process_title': 'Our Implementation Process',
            'process_step_1': 'We start by listening — understanding your current systems, pain points, and goals.',
            'process_step_2': 'Based on our assessment, we prescribe tailored solutions built for your specific context.',
            'process_step_3': 'Systems need to evolve with your business. We provide ongoing support and refinement.',
            'cta_title': 'Ready to Build Better Systems?',
            'cta_description': "Let's Diagnose what's slowing you down and design systems that work.",
            'cta_button_text': 'Book a free operational assessment'
        }
    )
    
    if created:
        print("Created Operational Systems page content")
    else:
        print("Operational Systems page content already exists")
    
    # Living Systems Page
    living_systems, created = LivingSystemsPageContent.objects.update_or_create(
        is_active=True,
        defaults={
            'hero_title': 'Living Systems & Regeneration',
            'hero_subtitle': 'We work with living systems — landscapes, forests, oceans, and ecosystems — to design regenerative solutions that bring life back to degraded environments.',
            'hero_description': 'From farms and urban plots to coastlines, regenerative agriculture and circular economy design, we help organizations create systems that restore biodiversity, sequester carbon, and build resilience.',
            'services_title': 'Our Regenerative Services',
            'service_1_title': 'Ecosystem Restoration',
            'service_1_description': 'Restore and regenerate natural systems for long-term sustainability',
            'service_2_title': 'Sustainable Production',
            'service_2_description': 'Design production systems that work with natural processes',
            'service_3_title': 'Environmental Monitoring',
            'service_3_description': 'Track and measure environmental impact and recovery',
            'process_title': 'Our Regenerative Approach',
            'process_step_1': 'We begin with comprehensive site assessment and system analysis to understand current ecological conditions, resource flows, and regenerative potential.',
            'process_step_2': 'Once you receive the regeneration report, you choose your path forward: Use the report independently to guide internal regeneration efforts or engage ORR for ongoing implementation support through tailored partnership.',
            'process_step_3': 'For ongoing partnerships, we move into implementation and stewardship phases. We execute regenerative solutions, build ecological infrastructure, and establish monitoring systems.',
            'cta_title': 'Ready to Work With Your Living Systems, Not Against Them?',
            'cta_description': "Let's help your business discover and design systems that regenerate rather than deplete.",
            'cta_button_text': 'Book a free Living Systems assessment'
        }
    )
    
    if created:
        print("Created Living Systems page content")
    else:
        print("Living Systems page content already exists")
    
    print("\nService pillar content setup complete!")
    print(f"Strategic Advisory ID: {strategic_advisory.id}")
    print(f"Operational Systems ID: {operational_systems.id}")
    print(f"Living Systems ID: {living_systems.id}")

if __name__ == '__main__':
    create_service_pillar_content()