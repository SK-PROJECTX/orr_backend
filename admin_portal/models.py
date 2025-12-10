from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from common.models import Audit


class AdminRole(models.Model):
    """Admin roles with flexible permissions"""

    ROLE_CHOICES = [
        ("super_admin", "Super Admin"),
        ("admin", "Admin"),
        ("operator", "Operator/Support"),
        ("content_editor", "Content Editor"),
    ]

    name = models.CharField(max_length=50, choices=ROLE_CHOICES, unique=True)
    description = models.TextField(blank=True)

    # Permissions
    can_manage_users = models.BooleanField(default=False)
    can_view_all_clients = models.BooleanField(default=False)
    can_edit_clients = models.BooleanField(default=False)
    can_manage_tickets = models.BooleanField(default=False)
    can_manage_meetings = models.BooleanField(default=False)
    can_create_content = models.BooleanField(default=False)
    can_publish_content = models.BooleanField(default=False)
    can_view_analytics = models.BooleanField(default=False)
    can_view_billing = models.BooleanField(default=False)
    can_manage_settings = models.BooleanField(default=False)
    can_view_ai_logs = models.BooleanField(default=False)

    def __str__(self):
        return self.get_name_display()


class AdminProfile(Audit):
    """Extended profile for admin users"""

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="admin_profile"
    )
    role = models.ForeignKey(AdminRole, on_delete=models.SET_NULL, null=True)
    department = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.role}"


class Client(Audit):
    """Client model for admin portal"""

    STAGE_CHOICES = [
        ("discover", "Discover"),
        ("diagnose", "Diagnose"),
        ("design", "Design"),
        ("deploy", "Deploy"),
        ("grow", "Grow"),
    ]

    PILLAR_CHOICES = [
        ("strategic", "Strategic Advisory & Compliance"),
        ("digital", "Digital Systems, Automation & AI"),
        ("living", "Living Systems & Regeneration"),
    ]

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="client_profile"
    )
    company = models.CharField(max_length=200)
    role = models.CharField(max_length=100, blank=True)
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default="discover")
    primary_pillar = models.CharField(max_length=20, choices=PILLAR_CHOICES)
    secondary_pillars = models.JSONField(default=list, blank=True)

    # Admin fields
    assigned_admin = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_clients",
    )
    internal_notes = models.TextField(blank=True)
    is_portal_active = models.BooleanField(default=True)
    last_activity = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.company}"


class Ticket(Audit):
    """Payment and support ticket system"""

    STATUS_CHOICES = [
        ("new", "New"),
        ("processing", "Processing Payment"),
        ("payment_failed", "Payment Failed"),
        ("payment_disputed", "Payment Disputed"),
        ("refund_requested", "Refund Requested"),
        ("refund_processed", "Refund Processed"),
        ("resolved", "Resolved"),
        ("archived", "Archived"),
    ]

    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("normal", "Normal"),
        ("high", "High"),
        ("urgent", "Urgent"),
    ]

    SOURCE_CHOICES = [
        ("payment_webhook", "Payment Webhook"),
        ("billing_portal", "Billing Portal"),
        ("subscription_change", "Subscription Change"),
        ("manual_request", "Manual Request"),
        ("client_inquiry", "Client Inquiry"),
    ]

    ticket_id = models.CharField(max_length=20, unique=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="tickets")
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tickets",
    )

    subject = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    priority = models.CharField(
        max_length=10, choices=PRIORITY_CHOICES, default="normal"
    )
    source = models.CharField(
        max_length=20, choices=SOURCE_CHOICES, default="manual_request"
    )

    # Content
    description = models.TextField()
    internal_notes = models.TextField(blank=True)

    # Payment relationships (required - all tickets must be payment-related)
    related_invoice = models.ForeignKey(
        "payment.Invoice", on_delete=models.CASCADE, null=True, blank=True
    )
    related_subscription = models.ForeignKey(
        "payment.Subscription", on_delete=models.CASCADE, null=True, blank=True
    )
    
    # Payment specific fields
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True)
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.related_invoice and not self.related_subscription:
            raise ValidationError("Ticket must be linked to either an invoice or subscription.")
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.ticket_id:
            self.ticket_id = (
                f"TKT-{timezone.now().strftime('%Y%m%d')}-{self.pk or '001'}"
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.ticket_id} - {self.subject}"


class TicketMessage(Audit):
    """Messages within tickets"""

    ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, related_name="messages"
    )
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_internal = models.BooleanField(default=False)  # Internal notes vs client-visible

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.ticket.ticket_id} - {self.sender.username}"


class Content(Audit):
    """Content management for client portal"""

    TYPE_CHOICES = [
        ("faq", "FAQ"),
        ("article", "Article"),
        ("checklist", "Checklist"),
        ("template", "Template"),
        ("guide", "Guide"),
    ]

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
        ("archived", "Archived"),
    ]

    STAGE_CHOICES = [
        ("discover", "Discover"),
        ("diagnose", "Diagnose"),
        ("design", "Design"),
        ("deploy", "Deploy"),
        ("grow", "Grow"),
    ]

    PILLAR_CHOICES = [
        ("strategic", "Strategic Advisory & Compliance"),
        ("digital", "Digital Systems, Automation & AI"),
        ("living", "Living Systems & Regeneration"),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    summary = models.TextField(blank=True)
    content = models.TextField()
    content_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")

    # Categorization
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES)
    pillars = models.JSONField(default=list)  # Multiple pillars allowed

    # Files
    attachment = models.FileField(
        upload_to="content_attachments/", blank=True, null=True
    )

    # Metadata
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    published_at = models.DateTimeField(null=True, blank=True)
    version = models.PositiveIntegerField(default=1)

    # Analytics
    view_count = models.PositiveIntegerField(default=0)
    download_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Meeting(Audit):
    """Meeting management system"""

    TYPE_CHOICES = [
        ("discovery", "Discovery Meeting"),
        ("follow_up", "Follow-up"),
        ("report_review", "Report Review"),
        ("consultation", "Consultation"),
    ]

    STATUS_CHOICES = [
        ("requested", "Requested"),
        ("confirmed", "Confirmed"),
        ("rescheduled", "Rescheduled"),
        ("declined", "Declined"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="meetings"
    )
    meeting_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="requested"
    )


    requested_datetime = models.DateTimeField()
    confirmed_datetime = models.DateTimeField(null=True, blank=True)
    end_datetime = models.DateTimeField(null=True, blank=True)
    duration_minutes = models.PositiveIntegerField(default=60)


    agenda = models.TextField(blank=True)
    meeting_notes = models.TextField(blank=True)
    internal_notes = models.TextField(blank=True)

    # Assignment
    host = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="hosted_meetings",
    )

    # Integration
    calendar_event_id = models.CharField(max_length=200, blank=True)
    meeting_link = models.URLField(blank=True)

    @property
    def duration_hours(self):
         # If Calendly sent confirmed start & end time:
        if self.confirmed_datetime and hasattr(self, "end_datetime") and self.end_datetime:
            delta = self.end_datetime - self.confirmed_datetime
            minutes = delta.total_seconds() / 60
            return minutes / 60

        return self.duration_minutes / 60


    @property
    def event_date(self):
        dt = self.confirmed_datetime or self.requested_datetime
        return dt.date()

    @property
    def event_time(self):
        dt = self.confirmed_datetime or self.requested_datetime
        return dt.strftime("%H:%M")

    @property
    def label(self):
        today = timezone.now().date()
        diff = (self.event_date - today).days

        if diff < 0:
            return "Completed"
        if diff == 0:
            return "Today"
        if diff == 1:
            return "Tomorrow"
        return f"{diff} days left"

    @property
    def color(self):
        mapping = {
            "requested": "#60A5FA",  # blue
            "confirmed": "#4ADE80",  # green
            "rescheduled": "#FACC15",  # yellow
            "declined": "#F87171",  # red
            "completed": "#9CA3AF",  # gray
            "cancelled": "#EF4444",  # red
        }
        return mapping.get(self.status, "#6B7280")

    @property
    def title(self):
        return self.get_meeting_type_display()

    def __str__(self):
        return f"{self.client.user.get_full_name()} - {self.get_meeting_type_display()}"


class AIConversation(Audit):
    """AI chat logs and oversight"""

    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="ai_conversations"
    )
    session_id = models.CharField(max_length=100)

    # Conversation data
    messages = models.JSONField(default=list)  # Store full conversation
    summary = models.TextField(blank=True)

    # Escalation
    escalated_to_ticket = models.BooleanField(default=False)
    escalation_reason = models.TextField(blank=True)

    # Quality control
    needs_improvement = models.BooleanField(default=False)
    improvement_notes = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"{self.client.user.get_full_name()} - {self.session_id}"


class SystemNotification(Audit):
    """System-wide notifications for admin users"""

    TYPE_CHOICES = [
        ("ticket_created", "New Ticket"),
        ("ticket_assigned", "Ticket Assigned"),
        ("meeting_requested", "Meeting Requested"),
        ("meeting_updated", "Meeting Updated"),
        ("system_error", "System Error"),
        ("ai_improvement", "AI Needs Improvement"),
    ]

    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    title = models.CharField(max_length=200)
    message = models.TextField()

    # Targeting
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="admin_notifications"
    )
    is_read = models.BooleanField(default=False)

    # Related objects
    related_ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, null=True, blank=True
    )
    related_meeting = models.ForeignKey(
        Meeting, on_delete=models.CASCADE, null=True, blank=True
    )
    related_client = models.ForeignKey(
        Client, on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - {self.recipient.username}"


class SystemSettings(models.Model):
    """System configuration settings"""

    # Branding
    company_name = models.CharField(max_length=200, default="ORR")
    logo = models.ImageField(upload_to="branding/", blank=True, null=True)
    primary_color = models.CharField(max_length=7, default="#007bff")
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)

    # Meeting settings
    default_meeting_duration = models.PositiveIntegerField(default=60)  # minutes
    meeting_buffer_time = models.PositiveIntegerField(default=15)  # minutes
    business_hours_start = models.TimeField(default="09:00")
    business_hours_end = models.TimeField(default="17:00")

    # Notification settings
    email_notifications_enabled = models.BooleanField(default=True)
    notification_email = models.EmailField(blank=True)

    # Legal
    privacy_policy_url = models.URLField(blank=True)
    terms_of_service_url = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "System Settings"
        verbose_name_plural = "System Settings"

    def __str__(self):
        return f"System Settings - {self.company_name}"


class AuditLog(models.Model):
    """Audit trail for compliance"""

    ACTION_CHOICES = [
        ("login", "User Login"),
        ("logout", "User Logout"),
        ("create", "Create"),
        ("update", "Update"),
        ("delete", "Delete"),
        ("publish", "Publish Content"),
        ("archive", "Archive Content"),
        ("role_change", "Role Change"),
        ("permission_change", "Permission Change"),
        ("data_export", "Data Export"),
        ("data_delete", "Data Delete"),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=100, blank=True)
    object_id = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.user} - {self.action} - {self.timestamp}"


class ClientDocument(Audit):
    """Documents specific to clients"""

    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="documents"
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    document = models.FileField(upload_to="client_documents/")
    document_type = models.CharField(max_length=50, blank=True)

    # Access control
    is_visible_to_client = models.BooleanField(default=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    # Analytics
    download_count = models.PositiveIntegerField(default=0)
    last_accessed = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.client.user.get_full_name()} - {self.title}"
