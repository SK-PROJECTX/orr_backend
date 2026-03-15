from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from common.models import Audit
from django.core.validators import MinLengthValidator


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
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="supports",
        null=True,
        blank=True,
    )
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
    message = models.TextField(blank=True)
    is_read = models.BooleanField(default=False)
    metadata = models.JSONField(blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["-created_at"]), models.Index(fields=["user"])]

    def __str__(self):
        return f"{self.title} - {self.user}"



class OnboardingQuestionnaire(Audit):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='onboarding')
    is_completed = models.BooleanField(default=False)
    jurisdiction = models.CharField(max_length=50, choices=[
        ('malta', 'Malta'),
        ('eu_non_malta', 'EU (non-Malta)'),
        ('non_eu', 'Non-EU'),
        ('other', 'Other (specify)'),
    ])
    jurisdiction_other = models.CharField(max_length=100, blank=True)

    language = models.CharField(max_length=20, choices=[
        ('en', 'English'), ('mt', 'Maltese'), ('it', 'Italian'), ('other', 'Other (specify)')
    ])
    language_other = models.CharField(max_length=100, blank=True)

    keyboard_layout = models.CharField(max_length=20, choices=[
        ('en_us', 'EN-US'), ('en_uk', 'EN-UK'), ('mt', 'MT'), ('it', 'IT'), ('other', 'Other')
    ])
    keyboard_other = models.CharField(max_length=100, blank=True)

    date_format = models.CharField(max_length=20, choices=[
        ('dd_mm_yyyy', 'DD/MM/YYYY'), ('mm_dd_yyyy', 'MM/DD/YYYY')
    ])
    time_format_24h = models.BooleanField(default=True)   
    accepted_service_agreement = models.BooleanField(default=False)
    portal_interests = models.JSONField(default=list)  
    portal_interests_other = models.TextField(blank=True)

    user_type = models.CharField(max_length=50, choices=[
        ('founder', 'Founder / Entrepreneur'),
        ('small_business', 'Small business owner'),
        ('corporate', 'Corporate representative'),
        ('public_ngo', 'Public sector / NGO'),
        ('academic', 'Researcher / Academic'),
        ('professional', 'Individual professional'),
        ('other', 'Other (specify)'),
    ])
    user_type_other = models.CharField(max_length=100, blank=True)

    project_stage = models.CharField(max_length=50, choices=[
        ('exploration', 'Early Exploration'),
        ('pre_startup', 'Pre-Startup / Planning'),
        ('operational', 'Operational but seeking optimisation'),
        ('scaling', 'Scaling / Growth'),
        ('unsure', 'Unsure'),
    ])

    orr_pillars = models.JSONField(default=list) 

    has_active_project = models.CharField(max_length=10, choices=[
        ('yes', 'Yes'), ('no', 'No'), ('maybe', 'Maybe')
    ])
    project_description = models.TextField(blank=True, validators=[MinLengthValidator(10)])
    challenges = models.JSONField(default=list)
    challenges_other = models.TextField(blank=True)

    meeting_format = models.CharField(max_length=20, choices=[
        ('video', 'Online (video)'),
        ('phone', 'Phone call'),
        ('in_person', 'In-person (subject to availability)'),
    ])

    communication_tone = models.JSONField(default=list)

    notification_preference = models.CharField(max_length=20, choices=[
        ('email', 'Email'),
        ('portal_only', 'In-portal notifications only'),
        ('both', 'Both'),
    ])
    ai_specialist_domains = models.JSONField(default=list)
    ai_specialist_other = models.TextField(blank=True)
    additional_context = models.TextField(blank=True)

    class Meta:
        verbose_name = "Onboarding Questionnaire"
        verbose_name_plural = "Onboarding Questionnaires"

    def __str__(self):
        return f"Onboarding - {self.user.get_full_name() or self.user.email}"