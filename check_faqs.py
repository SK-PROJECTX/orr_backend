import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from admin_portal.models import FAQ

faqs = FAQ.objects.all()
for faq in faqs:
    print("EN:", faq.question_en)
    print("IT:", faq.question_it)
    print("---")
