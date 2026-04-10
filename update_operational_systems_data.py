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

from admin_portal.models_cms import OperationalSystemsPageContent

def update_operational_systems_data():
    """Update Operational Systems page with comprehensive case example data"""
    
    # Get or create the page content
    page_content, created = OperationalSystemsPageContent.objects.get_or_create(
        is_active=True,
        defaults={'hero_title': 'Operational Systems & Infrastructure'}
    )
    
    # Update case example fields
    page_content.case_challenge = "A mid-sized manufacturing company was experiencing significant operational inefficiencies, with production delays, quality issues, and rising costs. Manual processes dominated their workflow, leading to errors and inconsistent output."
    
    page_content.case_solution = "ORR conducted a comprehensive operational assessment, mapping all processes and identifying critical bottlenecks. We delivered a detailed optimization report with workflow redesign, quality control improvements, and automation opportunities."
    
    page_content.case_result = "Following ORR's recommendations, the company implemented standardized processes and automated key workflows, resulting in a 35% reduction in production time and 50% fewer quality defects. Overall operational costs decreased by 25% while customer satisfaction improved significantly."
    
    page_content.case_image_alt = "Manufacturing facility showing optimized workflow and automated systems"
    
    # Save the updated content
    page_content.save()
    
    print("✅ Operational Systems page case example data updated successfully!")
    print(f"Challenge: {page_content.case_challenge[:100]}...")
    print(f"Solution: {page_content.case_solution[:100]}...")
    print(f"Result: {page_content.case_result[:100]}...")

if __name__ == '__main__':
    update_operational_systems_data()