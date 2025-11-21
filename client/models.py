from ..common.models import Audit
from django.contrib.auth.models import User
from django.db import models

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
        blank=True
    )
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    language = models.CharField(max_length=50, default="en")
    timezone = models.CharField(max_length=100, default="UTC")
    profile_pic = models.ImageField(upload_to="profile_pics/", blank=True, null=True)
    bio_text = models.TextField(blank=True)
    bio_attachment = models.FileField(
        upload_to="profile_bio_attachments/",
        blank=True,
        null=True
    )
    def __str__(self):
        return f"{self.user.username}'s Profile"
   