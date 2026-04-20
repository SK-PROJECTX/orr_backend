import os
import sys
import django

# Set up Django FIRST
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
            'rest_framework',
            'modeltranslation',
        ],
        MIDDLEWARE=[
            'django.middleware.locale.LocaleMiddleware',
        ],
        LANGUAGES=(
            ('en', 'English'),
            ('it', 'Italian'),
        ),
        MODELTRANSLATION_DEFAULT_LANGUAGE='en',
        REST_FRAMEWORK={
            'DEFAULT_RENDERER_CLASSES': [
                'rest_framework.renderers.JSONRenderer',
            ],
            'TEST_REQUEST_RENDERER_CLASSES': [
                'rest_framework.renderers.JSONRenderer',
            ],
        },
        SECRET_KEY='diagnostic-key',
    )
    django.setup()

# NOW import rest_framework and others
from rest_framework.test import APIRequestFactory
from django.utils import translation
from admin_portal.v1.views.cms import AllContentView

factory = APIRequestFactory()

def test_lang(lang_code):
    print(f"\n--- Testing language: {lang_code} ---")
    translation.activate(lang_code)
    request = factory.get(f'/admin-portal/v1/cms/all-content/?lang={lang_code}')
    # Set the language in the request object as well
    request.LANGUAGE_CODE = lang_code
    
    view = AllContentView.as_view()
    try:
        response = view(request)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("Success! Checking sample field...")
            # print(response.data.get('data', {}).get('homepage', {}).get('hero_title'))
        else:
            print(f"Error Response Data: {response.data}")
    except Exception as e:
        import traceback
        print(f"Exception occurred: {str(e)}")
        traceback.print_exc()

test_lang('en')
test_lang('it')
