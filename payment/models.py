from django.contrib.auth.models import User
from django.db import models

from common.models import Audit


class PricingPlan(Audit):
    BILLING_TYPE_CHOICES = [
        ("monthly", "Monthly"),
        ("metered", "Per Hour / Metered"),
    ]
    name = models.CharField(max_length=100)
    stripe_price_id = models.CharField(max_length=200)
    amount = models.IntegerField()  # cents
    billing_type = models.CharField(max_length=20, choices=BILLING_TYPE_CHOICES)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.billing_type})"


class Subscription(Audit):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="subscription"
    )
    stripe_subscription_id = models.CharField(max_length=255, unique=True)
    stripe_customer_id = models.CharField(max_length=255)
    plan = models.ForeignKey(PricingPlan, on_delete=models.SET_NULL, null=True)
    plan_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    current_period_end = models.DateTimeField(null=True, blank=True)
    used_hours = models.FloatField(null=True, blank=True)

    
    def __str__(self):
        return f"{self.user} -> {self.plan_name}"


class Invoice(Audit):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stripe_invoice_id = models.CharField(max_length=255, unique=True)
    billing_title = models.CharField(max_length=255)
    status = models.CharField(max_length=20)
    billing_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    plan = models.CharField(max_length=50)
    users = models.IntegerField(default=1)
    invoice_pdf = models.URLField(null=True, blank=True)
    hosted_invoice_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"Invoice {self.stripe_invoice_id}"
