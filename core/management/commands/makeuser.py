from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from decouple import config
User = get_user_model()

class Command(BaseCommand):
    help = "Create a superuser for staging if it doesn't exist"

    def handle(self, *args, **kwargs):
        username = config("DJANGO_SUPERUSER_USERNAME")
        email = config("DJANGO_SUPERUSER_EMAIL")
        password = config("DJANGO_SUPERUSER_PASSWORD")

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f"Superuser '{username}' already exists."))
        else:
            User.objects.createsuperuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' created successfully!"))
