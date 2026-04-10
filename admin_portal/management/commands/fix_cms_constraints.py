from django.core.management.base import BaseCommand
from django.db import connection, transaction
from admin_portal.models_cms import ContentCard, ProcessStep, ServiceStage, ServicePillar, PolicyItem
import json


class Command(BaseCommand):
    help = 'Fix CMS data constraints and validate existing data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be fixed without making changes',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No changes will be made'))
        
        # Fix database constraints first
        self.fix_database_constraints(dry_run)
        
        # Validate and fix existing data
        self.validate_content_cards(dry_run)
        self.validate_other_cms_models(dry_run)
        
        self.stdout.write(self.style.SUCCESS('CMS data validation and fixes completed'))

    def fix_database_constraints(self, dry_run):
        """Fix database field constraints"""
        self.stdout.write('Checking database constraints...')
        
        with connection.cursor() as cursor:
            # Check for varchar(50) constraints in CMS tables
            cursor.execute("""
                SELECT table_name, column_name, character_maximum_length
                FROM information_schema.columns 
                WHERE table_schema = 'public' 
                AND table_name LIKE 'admin_portal_%'
                AND data_type = 'character varying'
                AND character_maximum_length < 500
                ORDER BY table_name, column_name
            """)
            
            constraints = cursor.fetchall()
            
            if constraints:
                self.stdout.write(f'Found {len(constraints)} fields with length constraints < 500:')
                for table, column, length in constraints:
                    self.stdout.write(f'  {table}.{column}: varchar({length})')
                
                if not dry_run:
                    self.stdout.write('Fixing constraints...')
                    for table, column, length in constraints:
                        try:
                            cursor.execute(f'ALTER TABLE {table} ALTER COLUMN {column} TYPE varchar(500)')
                            self.stdout.write(f'  Fixed {table}.{column}')
                        except Exception as e:
                            self.stdout.write(self.style.ERROR(f'  Failed to fix {table}.{column}: {e}'))
            else:
                self.stdout.write(self.style.SUCCESS('No problematic constraints found'))

    def validate_content_cards(self, dry_run):
        """Validate and fix ContentCard data"""
        self.stdout.write('Validating ContentCard data...')
        
        issues_found = 0
        
        for card in ContentCard.objects.all():
            card_issues = []
            
            # Check RichTextField content lengths
            for field_name in ['badge', 'title', 'button1_text', 'button2_text']:
                field_value = getattr(card, field_name)
                if isinstance(field_value, dict) and 'content' in field_value:
                    content = field_value['content']
                    if len(str(content)) > 2000:
                        card_issues.append(f'{field_name} content too long: {len(str(content))} chars')
                elif isinstance(field_value, str) and len(field_value) > 2000:
                    card_issues.append(f'{field_name} too long: {len(field_value)} chars')
            
            # Check image_url length
            if card.image_url and len(card.image_url) > 500:
                card_issues.append(f'image_url too long: {len(card.image_url)} chars')
            
            # Check content array
            if isinstance(card.content, list):
                for i, item in enumerate(card.content):
                    if isinstance(item, str) and len(item) > 5000:
                        card_issues.append(f'content[{i}] too long: {len(item)} chars')
            
            if card_issues:
                issues_found += 1
                self.stdout.write(f'ContentCard {card.id} issues:')
                for issue in card_issues:
                    self.stdout.write(f'  - {issue}')
                
                if not dry_run:
                    # Fix the issues by truncating content
                    self.fix_content_card_issues(card, card_issues)
        
        if issues_found == 0:
            self.stdout.write(self.style.SUCCESS('No ContentCard issues found'))
        else:
            self.stdout.write(f'Found issues in {issues_found} ContentCards')

    def fix_content_card_issues(self, card, issues):
        """Fix issues in a ContentCard"""
        try:
            # Truncate RichTextField content if too long
            for field_name in ['badge', 'title', 'button1_text', 'button2_text']:
                field_value = getattr(card, field_name)
                if isinstance(field_value, dict) and 'content' in field_value:
                    content = field_value['content']
                    if len(str(content)) > 2000:
                        field_value['content'] = str(content)[:1997] + '...'
                        setattr(card, field_name, field_value)
                elif isinstance(field_value, str) and len(field_value) > 2000:
                    setattr(card, field_name, field_value[:1997] + '...')
            
            # Truncate image_url if too long
            if card.image_url and len(card.image_url) > 500:
                card.image_url = card.image_url[:497] + '...'
            
            # Truncate content array items if too long
            if isinstance(card.content, list):
                for i, item in enumerate(card.content):
                    if isinstance(item, str) and len(item) > 5000:
                        card.content[i] = item[:4997] + '...'
            
            card.save()
            self.stdout.write(f'  Fixed ContentCard {card.id}')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'  Failed to fix ContentCard {card.id}: {e}'))

    def validate_other_cms_models(self, dry_run):
        """Validate other CMS models"""
        self.stdout.write('Validating other CMS models...')
        
        models_to_check = [
            (ProcessStep, ['step_number', 'title', 'subtitle', 'description']),
            (ServiceStage, ['title', 'subtitle', 'description']),
            (ServicePillar, ['title', 'description']),
            (PolicyItem, ['number', 'description']),
        ]
        
        total_issues = 0
        
        for model_class, fields_to_check in models_to_check:
            model_issues = 0
            
            for instance in model_class.objects.all():
                for field_name in fields_to_check:
                    field_value = getattr(instance, field_name)
                    
                    if isinstance(field_value, dict) and 'content' in field_value:
                        content = field_value['content']
                        if len(str(content)) > 2000:
                            model_issues += 1
                            self.stdout.write(f'{model_class.__name__} {instance.id}.{field_name} too long: {len(str(content))} chars')
                            
                            if not dry_run:
                                field_value['content'] = str(content)[:1997] + '...'
                                setattr(instance, field_name, field_value)
                                try:
                                    instance.save()
                                    self.stdout.write(f'  Fixed {model_class.__name__} {instance.id}.{field_name}')
                                except Exception as e:
                                    self.stdout.write(self.style.ERROR(f'  Failed to fix: {e}'))
                    
                    elif isinstance(field_value, str) and len(field_value) > 500:
                        model_issues += 1
                        self.stdout.write(f'{model_class.__name__} {instance.id}.{field_name} too long: {len(field_value)} chars')
                        
                        if not dry_run:
                            setattr(instance, field_name, field_value[:497] + '...')
                            try:
                                instance.save()
                                self.stdout.write(f'  Fixed {model_class.__name__} {instance.id}.{field_name}')
                            except Exception as e:
                                self.stdout.write(self.style.ERROR(f'  Failed to fix: {e}'))
            
            if model_issues == 0:
                self.stdout.write(self.style.SUCCESS(f'No issues found in {model_class.__name__}'))
            else:
                total_issues += model_issues
        
        if total_issues == 0:
            self.stdout.write(self.style.SUCCESS('No issues found in other CMS models'))