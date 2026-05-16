import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from admin_portal.models import ClientDocument

docs = ClientDocument.objects.filter(document__isnull=False, document_type='')
print(f"Found {docs.count()} documents without type.")

for doc in docs:
    ext = os.path.splitext(doc.document.name)[1].lower()
    if ext:
        doc.document_type = ext.replace('.', '')
        doc.save()
        print(f"Updated {doc.title} to type {doc.document_type}")

print("Done.")
