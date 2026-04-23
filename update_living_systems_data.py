#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_dir)

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.development')
django.setup()

from admin_portal.models_cms import LivingSystemsPageContent

def update_living_systems_data():
    """Update Living Systems page with comprehensive case example data"""
    
    print("Updating Living Systems page content...")
    
    # Get or create the page content
    page_content, created = LivingSystemsPageContent.objects.get_or_create(
        is_active=True,
        defaults={'hero_title': 'Living Systems & Regeneration'}
    )
    
    # Update core fields
    page_content.hero_title = 'Living Systems & Regeneration'
    page_content.hero_subtitle = 'Support for land, water, species and ecosystems — from production systems to restoration and incident response.'
    page_content.hero_description = 'We help organizations integrate regenerative practices that foster both business outcomes and environmental health.'
    
    # Update case example fields
    page_content.case_challenge = "A large agricultural estate was facing soil degradation and declining biodiversity, leading to reduced yields and increased vulnerability to climate-related stresses. Traditional farming methods were no longer sufficient to sustain the land's productivity."
    
    page_content.case_solution = "ORR implemented a living systems approach, introducing regenerative agriculture techniques such as cover cropping, diverse crop rotations, and managed grazing. We also established biodiversity corridors and restored local water cycles to enhance the estate's natural resilience."
    
    page_content.case_result = "Within three years, the estate saw a significant improvement in soil health and a 20% increase in crop yields. Biodiversity flourished, with the return of several native species. The estate is now more resilient to drought and extreme weather events, and has successfully transitioned to a more sustainable and profitable operating model."
    
    page_content.case_image_alt = "Restored agricultural landscape with diverse crops and thriving ecosystems"
    
    # Save the updated content
    page_content.save()
    
    print("Living Systems page data updated successfully!")

if __name__ == '__main__':
    update_living_systems_data()
