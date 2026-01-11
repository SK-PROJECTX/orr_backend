from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
import os
from admin_portal.models import AdminProfile, AdminRole, SystemSettings


class Command(BaseCommand):
    help = "Setup initial admin portal data"

    def handle(self, *args, **options):
        self.stdout.write("Setting up admin portal...")

        # Create admin roles
        self.create_admin_roles()

        # Create system settings
        self.create_system_settings()

        # Create superuser if not exists
        self.create_superuser()

        self.stdout.write(
            self.style.SUCCESS("Admin portal setup completed successfully!")
        )
        self.stdout.write(
            self.style.WARNING(
                "Default login: admin / admin123 (CHANGE IN PRODUCTION!)"
            )
        )

    def create_admin_roles(self):
        """Create default admin roles"""
        roles_data = [
            {
                "name": "super_admin",
                "description": "Super Administrator with full access",
                "permissions": {
                    "can_manage_users": True,
                    "can_view_all_clients": True,
                    "can_edit_clients": True,
                    "can_manage_tickets": True,
                    "can_manage_meetings": True,
                    "can_create_content": True,
                    "can_publish_content": True,
                    "can_view_analytics": True,
                    "can_view_billing": True,
                    "can_manage_settings": True,
                    "can_view_ai_logs": True,
                },
            },
            {
                "name": "admin",
                "description": "Administrator with limited access",
                "permissions": {
                    "can_manage_users": False,
                    "can_view_all_clients": True,
                    "can_edit_clients": True,
                    "can_manage_tickets": True,
                    "can_manage_meetings": True,
                    "can_create_content": True,
                    "can_publish_content": False,
                    "can_view_analytics": True,
                    "can_view_billing": False,
                    "can_manage_settings": False,
                    "can_view_ai_logs": True,
                },
            },
            {
                "name": "operator",
                "description": "Operator focused on tickets and meetings",
                "permissions": {
                    "can_manage_users": False,
                    "can_view_all_clients": False,
                    "can_edit_clients": False,
                    "can_manage_tickets": True,
                    "can_manage_meetings": True,
                    "can_create_content": False,
                    "can_publish_content": False,
                    "can_view_analytics": False,
                    "can_view_billing": False,
                    "can_manage_settings": False,
                    "can_view_ai_logs": False,
                },
            },
            {
                "name": "content_editor",
                "description": "Content Editor focused on content management",
                "permissions": {
                    "can_manage_users": False,
                    "can_view_all_clients": False,
                    "can_edit_clients": False,
                    "can_manage_tickets": False,
                    "can_manage_meetings": False,
                    "can_create_content": True,
                    "can_publish_content": True,
                    "can_view_analytics": False,
                    "can_view_billing": False,
                    "can_manage_settings": False,
                    "can_view_ai_logs": False,
                },
            },
        ]

        for role_data in roles_data:
            role, created = AdminRole.objects.get_or_create(
                name=role_data["name"],
                defaults={
                    "description": role_data["description"],
                    **role_data["permissions"],
                },
            )
            if created:
                self.stdout.write(f"Created role: {role.get_name_display()}")
            else:
                self.stdout.write(f"Role already exists: {role.get_name_display()}")

    def create_system_settings(self):
        """Create default system settings"""
        if not SystemSettings.objects.exists():
            SystemSettings.objects.create(
                company_name="ORR",
                primary_color="#007bff",
                contact_email="admin@orr.com",
                default_meeting_duration=60,
                meeting_buffer_time=15,
                email_notifications_enabled=True,
            )
            self.stdout.write("Created default system settings")
        else:
            self.stdout.write("System settings already exist")

    def create_superuser(self):
        """Create superuser with admin profile safely"""
        username = os.getenv("DJANGO_SUPERUSER_USERNAME", "admin")
        email = os.getenv("DJANGO_SUPERUSER_EMAIL", "info@orr.solution")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD", None)

        # Check if user with this username exists
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                first_name="Admin",
                last_name="User",
            )

            # Create admin profile
            super_admin_role = AdminRole.objects.get_or_create(name="super_admin")
            AdminProfile.objects.create(
                user=user, role=super_admin_role, department="Administration"
            )

            self.stdout.write(f"Created superuser: {username}/{password}")

            # Create sample data
            self.create_sample_data(user)
        else:
            self.stdout.write(f"Superuser '{username}' already exists")

    def create_sample_data(self, admin_user):
        """Create sample data for testing"""
        from django.utils.text import slugify

        from admin_portal.models import Content, SystemNotification

        # Sample content
        sample_content = [
            {
                "title": "Getting Started with ORR",
                "content_type": "guide",
                "stage": "discover",
                "pillars": ["strategic"],
                "summary": "A comprehensive guide to getting started with ORR services.",
                "content": "This guide will help you understand the basics of ORR and how to get started with our services.",
            },
            {
                "title": "Digital Transformation FAQ",
                "content_type": "faq",
                "stage": "design",
                "pillars": ["digital"],
                "summary": "Frequently asked questions about digital transformation.",
                "content": "Common questions and answers about digital transformation processes.",
            },
        ]

        for content_data in sample_content:
            content, created = Content.objects.get_or_create(
                title=content_data["title"],
                defaults={
                    "slug": slugify(content_data["title"]),
                    "content_type": content_data["content_type"],
                    "stage": content_data["stage"],
                    "pillars": content_data["pillars"],
                    "summary": content_data["summary"],
                    "content": content_data["content"],
                    "status": "published",
                    "author": admin_user,
                },
            )

            if created:
                self.stdout.write(f"Created sample content: {content.title}")

        # Welcome notification
        SystemNotification.objects.get_or_create(
            recipient=admin_user,
            title="Welcome to ORR Admin Portal",
            defaults={
                "notification_type": "system_error",
                "message": "Welcome to the ORR Admin Portal! Your system is ready to use.",
            },
        )

        self.stdout.write("Created sample data")
