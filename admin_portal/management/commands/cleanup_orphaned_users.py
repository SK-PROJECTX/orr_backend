from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from admin_portal.models import Client
from django.db import transaction


class Command(BaseCommand):
    help = 'Clean up orphaned users and fix client profile issues'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be done without making changes',
        )
        parser.add_argument(
            '--fix-orphans',
            action='store_true',
            help='Remove users without client profiles (except superusers)',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        fix_orphans = options['fix_orphans']
        
        self.stdout.write(self.style.SUCCESS('=== CLIENT PROFILE CLEANUP ==='))
        
        # Find users without client profiles
        orphaned_users = User.objects.filter(
            client_profile__isnull=True,
            is_superuser=False,
            is_staff=False
        )
        
        self.stdout.write(f"Found {orphaned_users.count()} orphaned users")
        
        if orphaned_users.exists():
            for user in orphaned_users:
                self.stdout.write(f"  - {user.username} ({user.email}) - Created: {user.date_joined}")
        
        # Find duplicate emails
        duplicate_emails = []
        all_emails = User.objects.values_list('email', flat=True)
        seen_emails = set()
        
        for email in all_emails:
            if email in seen_emails:
                duplicate_emails.append(email)
            else:
                seen_emails.add(email)
        
        if duplicate_emails:
            self.stdout.write(f"\nFound {len(duplicate_emails)} duplicate emails:")
            for email in duplicate_emails:
                users_with_email = User.objects.filter(email=email)
                self.stdout.write(f"  - {email}: {users_with_email.count()} users")
                for user in users_with_email:
                    has_client = Client.objects.filter(user=user).exists()
                    self.stdout.write(f"    * {user.username} (ID: {user.id}) - Has Client: {has_client}")
        
        # Fix orphaned users if requested
        if fix_orphans and not dry_run:
            with transaction.atomic():
                deleted_count = 0
                for user in orphaned_users:
                    self.stdout.write(f"Deleting orphaned user: {user.username} ({user.email})")
                    user.delete()
                    deleted_count += 1
                
                self.stdout.write(
                    self.style.SUCCESS(f"Deleted {deleted_count} orphaned users")
                )
        elif fix_orphans and dry_run:
            self.stdout.write(
                self.style.WARNING(f"DRY RUN: Would delete {orphaned_users.count()} orphaned users")
            )
        
        # Summary
        total_users = User.objects.count()
        total_clients = Client.objects.count()
        users_with_clients = Client.objects.values('user').distinct().count()
        
        self.stdout.write("\n=== SUMMARY ===")
        self.stdout.write(f"Total Users: {total_users}")
        self.stdout.write(f"Total Clients: {total_clients}")
        self.stdout.write(f"Users with Client Profiles: {users_with_clients}")
        self.stdout.write(f"Users without Client Profiles: {total_users - users_with_clients}")
        
        if not dry_run and not fix_orphans:
            self.stdout.write("\nTo fix orphaned users, run with --fix-orphans")
            self.stdout.write("To see what would be changed, run with --dry-run")