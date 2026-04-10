from django.core.management.base import BaseCommand
from admin_portal.models_cms import BusinessSystemSection


class Command(BaseCommand):
    help = 'Populate business system section with default data'

    def handle(self, *args, **options):
        # Create or update business system section
        section, created = BusinessSystemSection.objects.get_or_create(
            is_active=True,
            defaults={
                'title': 'Businesses as a Living System',
                'subtitle': 'Think of your organisation like a body',
                'card_1_title': 'Nervous System',
                'card_1_description': 'Communication, data flow, and decision-making pathways',
                'card_1_image': '/images/nervous_system.png',
                'card_2_title': 'Circulatory System', 
                'card_2_description': 'Cash flow, resource distribution, and value exchange',
                'card_2_image': '/images/circulatory_system.png',
                'card_3_title': 'Immune System',
                'card_3_description': 'Risk management, compliance, and protective measures',
                'card_3_image': '/images/immune_system.png'
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS('Successfully created business system section')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Business system section already exists')
            )