from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from admin_portal.models import AdminProfile, AdminRole


class Command(BaseCommand):
    help = 'Create a test user for CMS authentication'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, default='editor', help='Username for the test user')
        parser.add_argument('--password', type=str, default='editor123', help='Password for the test user')
        parser.add_argument('--email', type=str, default='editor@orr.com', help='Email for the test user')

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']
        email = options['email']

        # Create or get user
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'is_staff': True,
                'is_active': True,
            }
        )
        
        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(f'Created user: {username}')
        else:
            self.stdout.write(f'User {username} already exists')

        # Create or get admin role
        role, role_created = AdminRole.objects.get_or_create(
            name='content_editor',
            defaults={
                'description': 'Content Editor Role',
                'can_create_content': True,
                'can_publish_content': True,
                'can_manage_users': False,
                'can_manage_settings': False,
                'can_view_all_clients': False,
                'can_edit_clients': False,
                'can_manage_tickets': False,
                'can_manage_meetings': False,
            }
        )
        
        if role_created:
            self.stdout.write(f'Created role: content_editor')

        # Create or get admin profile
        profile, profile_created = AdminProfile.objects.get_or_create(
            user=user,
            defaults={
                'role': role,
                'is_active': True,
            }
        )
        
        if profile_created:
            self.stdout.write(f'Created admin profile for {username}')
        else:
            # Update existing profile
            profile.role = role
            profile.is_active = True
            profile.save()
            self.stdout.write(f'Updated admin profile for {username}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Test user setup complete!\n'
                f'Username: {username}\n'
                f'Password: {password}\n'
                f'Role: content_editor\n'
                f'Can edit content: {role.can_create_content}'
            )
        )