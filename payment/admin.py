from django.contrib import admin

from .models import Invoice, PricingPlan, Subscription


@admin.register(PricingPlan)
class PricingPlanAdmin(admin.ModelAdmin):
    list_display = ("name", "amount", "stripe_price_id", "created_at")
    search_fields = ("name", "stripe_price_id")
    list_filter = ("created_at",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "plan_name",
        "is_active",
        "current_period_end",
        "stripe_subscription_id",
    )
    search_fields = (
        "user__username",
        "user__email",
        "plan_name",
        "stripe_subscription_id",
    )
    list_filter = ("is_active", "plan_name", "current_period_end", "created_at")
    readonly_fields = ("created_at", "updated_at")


# -----------------------
#  INVOICE ADMIN
# -----------------------
@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        "stripe_invoice_id",
        "user",
        "billing_title",
        "status",
        "billing_date",
        "amount",
        "currency",
        "plan",
    )
    search_fields = (
        "stripe_invoice_id",
        "user__username",
        "user__email",
        "billing_title",
        "plan",
    )
    list_filter = ("status", "billing_date", "currency", "plan", "created_at")
    readonly_fields = ("created_at", "updated_at")
