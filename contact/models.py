from django.db import models
from common.models import Audit

class ContactMessage(Audit):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    subject = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.subject}"
