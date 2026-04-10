#!/usr/bin/env python
"""
Script to update Strategic Advisory page content with comprehensive data
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.development')
django.setup()

from admin_portal.models_cms import StrategicAdvisoryPageContent

def update_strategic_advisory_content():
    """Update Strategic Advisory page content with comprehensive data"""
    
    print("Updating Strategic Advisory page content...")
    
    # Get or create the content
    strategic_advisory, created = StrategicAdvisoryPageContent.objects.get_or_create(
        is_active=True,
        defaults={}
    )
    
    # Update with comprehensive data
    strategic_advisory.hero_title = 'Strategic Advisory & Compliance'
    strategic_advisory.hero_subtitle = 'We deliver clarity to complexity. From regulatory and sustainability frameworks to biotechnology and compliance consulting, our experts guide clients through evolving landscapes with confidence.'
    strategic_advisory.hero_description = 'Our approach combines deep technical insight with strategic foresight, ensuring every initiative is compliant, sustainable, and built for growth.'
    strategic_advisory.services_title = 'Our Strategic Services'
    strategic_advisory.service_1_title = 'Regulatory Compliance & Advisory'
    strategic_advisory.service_1_description = 'Navigate complex regulatory landscapes with confidence. We provide strategic guidance on compliance requirements, regulatory changes, and implementation strategies.'
    strategic_advisory.service_2_title = 'ESG & Sustainability Strategy'
    strategic_advisory.service_2_description = 'Develop comprehensive ESG frameworks that meet stakeholder expectations while driving business value. From carbon accounting to sustainability reporting.'
    strategic_advisory.service_3_title = 'Biotechnology & Life Sciences Consulting'
    strategic_advisory.service_3_description = 'Leverage our network of scientific experts to navigate the technical and regulatory complexities of biotechnology and life sciences.'
    
    # Process section
    strategic_advisory.process_title = 'Our Strategic Process'
    if hasattr(strategic_advisory, 'process_subtitle'):
        strategic_advisory.process_subtitle = 'Listen . Solve . Optimize'
    if hasattr(strategic_advisory, 'process_description'):
        strategic_advisory.process_description = 'Like your Business GP, we diagnose compliance challenges and prescribe strategic solutions tailored to your organization\'s unique context.'
    if hasattr(strategic_advisory, 'process_step_1_title'):
        strategic_advisory.process_step_1_title = 'Listen & Report'
    if hasattr(strategic_advisory, 'process_step_1_subtitle'):
        strategic_advisory.process_step_1_subtitle = '(Initial Discovery)'
    strategic_advisory.process_step_1 = 'We start with a focused initial meeting to understand your compliance challenges, regulatory environment, and strategic objectives.'
    if hasattr(strategic_advisory, 'process_step_2_title'):
        strategic_advisory.process_step_2_title = 'Decide: Document or Partnership'
    strategic_advisory.process_step_2 = 'Once you receive the report, you choose your path forward: Use the report independently or engage ORR for ongoing implementation support.'
    if hasattr(strategic_advisory, 'process_step_3_title'):
        strategic_advisory.process_step_3_title = 'Optimize (For Clients Who Continue)'
    strategic_advisory.process_step_3 = 'For clients who choose ongoing partnership, we move into implementation and optimization.'
    
    # Network section
    if hasattr(strategic_advisory, 'network_title'):
        strategic_advisory.network_title = 'The ORR Network Advantage'
    if hasattr(strategic_advisory, 'network_description'):
        strategic_advisory.network_description = 'Complex compliance challenges require diverse expertise. We activate our global network of specialists to deliver comprehensive solutions.'
    if hasattr(strategic_advisory, 'network_cards'):
        strategic_advisory.network_cards = [
            {
                "title": "Legal & Regulatory Experts",
                "description": "Specialized attorneys and compliance professionals across multiple jurisdictions",
                "icon": "M12 3L1 9L12 15L21 12.35V17H23V9M5 13.18V17.18L12 21L19 17.18V13.18L12 17L5 13.18Z"
            },
            {
                "title": "Scientific Advisors",
                "description": "PhDs and researchers in biotechnology, environmental and computer science, and related fields",
                "icon": "M9.5 3A6.5 6.5 0 0 1 16 9.5C16 11.11 15.41 12.59 14.44 13.73L14.71 14H16L21 19L19 21L14 16V14.71L13.73 14.44C12.59 15.41 11.11 16 9.5 16A6.5 6.5 0 0 1 3 9.5A6.5 6.5 0 0 1 9.5 3M9.5 5C7 5 5 7 5 9.5S7 14 9.5 14 14 12 14 9.5 12 5 9.5 5Z"
            },
            {
                "title": "Industry Specialists",
                "description": "Sector-specific consultants with deep regulatory knowledge",
                "icon": "M12 15.5A3.5 3.5 0 0 1 8.5 12A3.5 3.5 0 0 1 12 8.5A3.5 3.5 0 0 1 15.5 12A3.5 3.5 0 0 1 12 15.5M19.43 12.98C19.47 12.66 19.5 12.33 19.5 12S19.47 11.34 19.43 11.02L21.54 9.37C21.73 9.22 21.78 8.95 21.66 8.73L19.66 5.27C19.54 5.05 19.27 4.96 19.05 5.05L16.56 6.05C16.04 5.65 15.48 5.32 14.87 5.07L14.49 2.42C14.46 2.18 14.25 2 14 2H10C9.75 2 9.54 2.18 9.51 2.42L9.13 5.07C8.52 5.32 7.96 5.66 7.44 6.05L4.95 5.05C4.73 4.96 4.46 5.05 4.34 5.27L2.34 8.73C2.21 8.95 2.27 9.22 2.46 9.37L4.57 11.02C4.53 11.34 4.5 11.67 4.5 12S4.53 12.66 4.57 12.98L2.46 14.63C2.27 14.78 2.21 15.05 2.34 15.27L4.34 18.73C4.46 18.95 4.73 19.03 4.95 18.95L7.44 17.94C7.96 18.34 8.52 18.68 9.13 18.93L9.51 21.58C9.54 21.82 9.75 22 10 22H14C14.25 22 14.46 21.82 14.49 21.58L14.87 18.93C15.48 18.68 16.04 18.34 16.56 17.94L19.05 18.95C19.27 19.03 19.54 18.95 19.66 18.73L21.66 15.27C21.78 15.05 21.73 14.78 21.54 14.63L19.43 12.98Z"
            }
        ]
    
    # Digital solutions section
    if hasattr(strategic_advisory, 'digital_title'):
        strategic_advisory.digital_title = 'Digital Solutions for'
    if hasattr(strategic_advisory, 'digital_subtitle'):
        strategic_advisory.digital_subtitle = 'Compliance Management'
    if hasattr(strategic_advisory, 'digital_description'):
        strategic_advisory.digital_description = 'We don\'t just advise — we build digital infrastructure to operationalize compliance:'
    if hasattr(strategic_advisory, 'digital_image_alt'):
        strategic_advisory.digital_image_alt = 'Network visualization showing connected nodes and data flows'
    if hasattr(strategic_advisory, 'digital_who_is_this_for'):
        strategic_advisory.digital_who_is_this_for = [
            "Self-employed professionals and consultants who need expert compliance guidance without hiring full-time staff",
            "Growing businesses entering regulated industries or expanding into new markets",
            "Startups in life sciences and biotech navigating complex regulatory pathways",
            "Professional service firms managing client compliance obligations",
            "Companies facing regulatory changes that impact their operations",
            "Businesses implementing ESG strategies to meet investor and stakeholder expectations"
        ]
    if hasattr(strategic_advisory, 'digital_features'):
        strategic_advisory.digital_features = [
            "Custom compliance management platforms with automated tracking",
            "Regulatory document repositories with version control and access management",
            "ESG data collection and reporting dashboards",
            "Audit trail systems with timestamped documentation",
            "Training management systems with certification tracking",
            "AI-powered regulatory monitoring and change detection",
            "Integrated risk assessment and mitigation tracking tools",
            "Automated compliance reporting and submission workflows"
        ]
    
    # Case example section
    if hasattr(strategic_advisory, 'case_challenge'):
        strategic_advisory.case_challenge = 'A cooperative operating in a niche market faced decreased profits and pressure from stakeholders to reverse the trend. The board understood the severity of the issue and recognized that scientific studies were essential to inform their strategic decisions. However, lacking scientific expertise internally, the cooperative was spending hundreds of thousands of euros on external scientific study reports with limited guidance on how to action the findings.'
    if hasattr(strategic_advisory, 'case_solution'):
        strategic_advisory.case_solution = 'ORR was brought in to assess the situation and provide strategic direction. Within days, we delivered a detailed report outlining the ideal modus operandi. The report covered market pricing for scientific analysis, relevant regulatory frameworks to guide compliance, and how to strategically increase the value of their niche market through product specialization — including a roadmap for PDO (Protected Designation of Origin) or IGP (Protected Geographical Indication) applications.'
    if hasattr(strategic_advisory, 'case_result'):
        strategic_advisory.case_result = 'Armed with ORR\'s strategic report, the cooperative immediately redirected their approach, significantly reducing unnecessary scientific study expenses while focusing resources on high-impact initiatives. The specialization strategy aimed them toward premium market segments, and the cooperative is now pursuing PDO certification to differentiate their product and command higher prices. Stakeholder confidence has been restored as profits begin to recover.'
    if hasattr(strategic_advisory, 'case_image_alt'):
        strategic_advisory.case_image_alt = 'Business documents and reports on a desk'
    
    # CTA section
    strategic_advisory.cta_title = 'Ready to Navigate Complexity with Confidence?'
    strategic_advisory.cta_description = 'Let\'s assess your compliance landscape and design strategies that protect and enable your growth.'
    strategic_advisory.cta_button_text = 'Book a free compliance assessment'
    
    strategic_advisory.save()
    
    print("Strategic Advisory content updated successfully!")
    print(f"Strategic Advisory ID: {strategic_advisory.id}")

if __name__ == '__main__':
    update_strategic_advisory_content()