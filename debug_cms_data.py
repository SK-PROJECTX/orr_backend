import os
import sys
import django

# Set up Django
db_pass = os.environ.get('DB_PASS')
if not db_pass:
    print("Error: DB_PASS environment variable not set.")
    sys.exit(1)

from django.conf import settings
if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'my_production_db',
                'USER': 'postgres',
                'PASSWORD': db_pass,
                'HOST': '34.134.52.218',
                'PORT': '5432',
                'OPTIONS': {
                    'sslmode': 'require',
                }
            }
        },
        INSTALLED_APPS=[
            'django.contrib.contenttypes',
            'django.contrib.auth',
            'admin_portal',
        ],
    )
    django.setup()
    import admin_portal.translation

from admin_portal.models_cms import ApproachSection, HomePage

print("Checking ApproachSection data...")
approaches = ApproachSection.objects.all()
print(f"Total ApproachSections: {approaches.count()}")
for a in approaches:
    print(f"ID: {a.id}, Title: {a.title}, Active: {a.is_active}")
    print(f"  Title IT: {a.title_it}")
    print(f"  P1 IT: {a.paragraph_1_it}")

print("\nChecking HomePage data...")
homepages = HomePage.objects.all()
print(f"Total HomePages: {homepages.count()}")
for h in homepages:
    print(f"ID: {h.id}, Title: {h.hero_title}, Active: {h.is_active}")
    print(f"  Hero Title IT: {h.hero_title_it}")
