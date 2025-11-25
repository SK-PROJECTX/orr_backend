from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from common.models import Audit


class Profile(Audit):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    nickname = models.CharField(max_length=100, blank=True)
    full_name = models.CharField(max_length=100, blank=True)
    gender = models.CharField(
        max_length=20,
        choices=[
            ("male", "Male"),
            ("female", "Female"),
            ("other", "Other"),
            ("prefer_not_say", "Prefer not to say"),
        ],
        blank=True,
    )
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    language = models.CharField(max_length=50, default="en")
    timezone = models.CharField(max_length=100, default="UTC")
    profile_pic = models.ImageField(upload_to="profile_pics/", blank=True, null=True)
    bio_text = models.TextField(blank=True)
    bio_attachment = models.FileField(
        upload_to="profile_bio_attachments/", blank=True, null=True
    )
    phone_number = models.CharField(max_length=20, blank=True)
    def __str__(self):
        return f"{self.user.username}'s Profile"


class ContactMessage(Audit):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    website = models.URLField(blank=True, null=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"
    
class Activity(Audit):
    ACTIVITY_TYPES = [
        ("DOCUMENT", "Document Uploaded"),
        ("TICKET", "Support Ticket Activity"),
        ("MEETING", "Meeting Activity"),
        ("CHECKLIST", "Checklist Update"),
        ("REPORT", "Report Update"),
        ("USER", "General User Activity"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="activities",
        null=True,
        blank=True,
    )
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    metadata = models.JSONField(blank=True, null=True)