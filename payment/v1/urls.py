from django.urls import path
from .views import CreateCheckoutSession, ChangePlanView, PauseSubscriptionView, BillingPortalView, StripeWebhookView, InvoiceListView, BillingHistoryView

urlpatterns = [
    path("payments/create-checkout/", CreateCheckoutSession.as_view()),
    path("subscriptions/change-plan/", ChangePlanView.as_view(), name="change-plan"),
    path("subscriptions/pause/", PauseSubscriptionView.as_view(), name="pause-subscription"),
    path("subscriptions/portal/", BillingPortalView.as_view(), name="billing-portal"),
    path("webhook/", StripeWebhookView.as_view()),
    path("billing-history/", BillingHistoryView.as_view()),
]