import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from admin_portal.models import ClientDocument

docs = ClientDocument.objects.all()
for doc in docs:
    print(f"ID: {doc.id}, Title: {doc.title}, Source: {doc.document_source}, Type: '{doc.document_type}', Doc: {doc.document.name if doc.document else 'None'}")
