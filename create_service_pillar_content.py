#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.development')
django.setup()

from admin_portal.models_cms import (
    StrategicAdvisoryPageContent,
    OperationalSystemsPageContent,
    LivingSystemsPageContent
)

def create_service_pillar_content():
    """Create initial content for service pillar pages"""
    
    # Strategic Advisory Page Content
    strategic_advisory, created = StrategicAdvisoryPageContent.objects.update_or_create(
        defaults={
            'hero_title': 'Strategic Advisory & Compliance',
            'hero_subtitle': 'Expert guidance for regulatory compliance and strategic planning',
            'hero_description': 'Navigate complex regulatory landscapes with confidence through our comprehensive advisory services.',
            'hero_image': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&h=600&fit=crop',
            'services_title': 'Our Strategic Services',
            'service_1_title': 'Regulatory Compliance',
            'service_1_description': 'Ensure full compliance with industry regulations and standards.',
            'service_2_title': 'Risk Assessment',
            'service_2_description': 'Identify and mitigate potential risks to your organization.',
            'service_3_title': 'Strategic Planning',
            'service_3_description': 'Develop comprehensive strategies for long-term success.',
            'process_title': 'Our Advisory Process',
            'process_step_1': 'Initial Assessment',
            'process_step_2': 'Strategy Development',
            'process_step_3': 'Implementation',
            'process_step_4': 'Monitoring & Review',
            'cta_title': 'Ready to Get Started?',
            'cta_description': 'Contact us today to discuss your strategic advisory needs.',
            'cta_button_text': 'Get Started',
            'meta_title': 'Strategic Advisory & Compliance - ORR Solutions',
            'meta_description': 'Expert strategic advisory and compliance services to help your organization navigate regulatory challenges.',
            'is_active': True
        }
    )
    
    if created:
        print("Created Strategic Advisory page content")
    else:
        print("Strategic Advisory page content already exists")
    
    # Operational Systems Page Content
    operational_systems, created = OperationalSystemsPageContent.objects.update_or_create(
        defaults={
            'hero_title': 'Operational Systems & Infrastructure',
            'hero_subtitle': 'Robust systems and infrastructure solutions',
            'hero_description': 'Build and maintain efficient operational systems that scale with your business needs.',
            'hero_image': 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&h=600&fit=crop',
            'services_title': 'Our Operational Services',
            'service_1_title': 'System Design',
            'service_1_description': 'Design scalable and efficient operational systems.',
            'service_2_title': 'Infrastructure Management',
            'service_2_description': 'Manage and optimize your IT infrastructure.',
            'service_3_title': 'Process Automation',
            'service_3_description': 'Automate key business processes for efficiency.',
            'process_title': 'Our Implementation Process',
            'process_step_1': 'Requirements Analysis',
            'process_step_2': 'System Design',
            'process_step_3': 'Implementation',
            'process_step_4': 'Testing & Deployment',
            'cta_title': 'Transform Your Operations',
            'cta_description': 'Let us help you build robust operational systems.',
            'cta_button_text': 'Contact Us',
            'meta_title': 'Operational Systems & Infrastructure - ORR Solutions',
            'meta_description': 'Professional operational systems and infrastructure services to optimize your business operations.',
            'is_active': True
        }
    )
    
    if created:
        print("Created Operational Systems page content")
    else:
        print("Operational Systems page content already exists")
    
    # Living Systems Page Content
    living_systems, created = LivingSystemsPageContent.objects.update_or_create(
        defaults={
            'hero_title': 'Living Systems & Sustainability',
            'hero_subtitle': 'Sustainable solutions for a better future',
            'hero_description': 'Create sustainable and regenerative systems that benefit both business and environment.',
            'hero_image': 'https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=800&h=600&fit=crop',
            'services_title': 'Our Sustainability Services',
            'service_1_title': 'Sustainability Assessment',
            'service_1_description': 'Evaluate your current sustainability practices and identify improvements.',
            'service_2_title': 'Green Technology',
            'service_2_description': 'Implement eco-friendly technologies and solutions.',
            'service_3_title': 'Regenerative Practices',
            'service_3_description': 'Develop practices that restore and regenerate natural systems.',
            'process_title': 'Our Sustainability Process',
            'process_step_1': 'Current State Analysis',
            'process_step_2': 'Sustainability Planning',
            'process_step_3': 'Implementation',
            'process_step_4': 'Impact Measurement',
            'cta_title': 'Build a Sustainable Future',
            'cta_description': 'Partner with us to create sustainable living systems.',
            'cta_button_text': 'Learn More',
            'meta_title': 'Living Systems & Sustainability - ORR Solutions',
            'meta_description': 'Sustainable living systems and environmental solutions for responsible business practices.',
            'is_active': True
        }
    )
    
    if created:
        print("Created Living Systems page content")
    else:
        print("Living Systems page content already exists")
    
    print("\nService pillar page content setup complete!")

if __name__ == '__main__':
    create_service_pillar_content()