from django.contrib import admin
from .models import PricingPlan, Subscription, Invoice, CheckoutSessionLog, StripeCustomer


@admin.register(PricingPlan)
class PricingPlanAdmin(admin.ModelAdmin):
    list_display = ("name", "billing_type", "amount", "stripe_price_id", "created_at")
    search_fields = ("name", "stripe_price_id")
    list_filter = ("billing_type",)
    ordering = ("-created_at",)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "plan_name",
        "stripe_customer_id",
        "stripe_subscription_id",
        "is_active",
        "current_period_end",
    )
    search_fields = (
        "user__username",
        "stripe_subscription_id",
        "stripe_customer_id",
        "plan_name",
    )
    list_filter = ("is_active",)
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        "stripe_invoice_id",
        "user",
        "status",
        "billing_title",
        "amount",
        "billing_date",
        "plan",
    )
    search_fields = ("stripe_invoice_id", "user__username", "billing_title")
    list_filter = ("status", "currency", "billing_date")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-billing_date",)

@admin.register(CheckoutSessionLog)
class CheckoutSessionLogAdmin(admin.ModelAdmin):
    list_display = ("stripe_session_id", "user", "plan", "status", "created_at", "updated_at")
    list_filter = ("status", "created_at", "plan")
    search_fields = ("stripe_session_id", "user__username", "plan__name")
    readonly_fields = ("stripe_session_id", "created_at", "updated_at")
    ordering = ("-created_at",)

@admin.register(StripeCustomer)
class StripeCustomerAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "stripe_customer_id",
        "stripe_card_id",
        "created_at",
        "updated_at",
    )
    list_select_related = ("user",)
    search_fields = (
        "user__username",
        "user__email",
        "stripe_customer_id",
    )
    readonly_fields = (
        "stripe_customer_id",
        "created_at",
        "updated_at",
    )
    ordering = ("-created_at",)

    fieldsets = (
        ("User", {
            "fields": ("user",),
        }),
        ("Stripe Details", {
            "fields": ("stripe_customer_id", "stripe_card_id"),
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
        }),
    )