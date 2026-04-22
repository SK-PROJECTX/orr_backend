from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    BillingHistoryView,
    BillingPortalView,
    ChangePlanView,
    CreateCheckoutSession,
    PauseSubscriptionView,
    PricingPlanViewSet,
    stripe_webhook,
    CreateSetupIntent,
    AddPaymentMethodView,
    DeletePaymentMethodView,
    CreateStripeCustomerView,
    ListPaymentMethodsView,
    GetStripeCustomerView,
    SubscriptionStatusAPIView,
)

from .wallet_views import (
    WalletBalanceView,
    TransactionListView,
    TopUpView,
    PayWithWalletView,
)

router = DefaultRouter()
router.register("pricing-plans", PricingPlanViewSet, basename="pricing-plan")

urlpatterns = [
    path("payments/create-checkout/", CreateCheckoutSession.as_view()),
    path("subscriptions/change-plan/", ChangePlanView.as_view(), name="change-plan"),
    path(
        "subscriptions/pause/",
        PauseSubscriptionView.as_view(),
        name="pause-subscription",
    ),
    path("subscriptions/portal/", BillingPortalView.as_view(), name="billing-portal"),
    path("billing-history/", BillingHistoryView.as_view()),
    path("stripe-webhook/", stripe_webhook, name="stripe-webhook"),
    path("setup-intent/", CreateSetupIntent.as_view(), name="create_setup_intent"),
     path(
        "user/create-stripe-customer/",
        CreateStripeCustomerView.as_view(),
        name="create-stripe-customer",
    ),
     path(
        "user/get-stripe-customer/",
        GetStripeCustomerView.as_view(),
        name="get-stripe-customer",
    ),

    path(
        "user/add-payment-method/",
        AddPaymentMethodView.as_view(),
        name="add-payment-method",
    ),
    path(
        "user/payment-methods/",
        ListPaymentMethodsView.as_view(),
        name="list-payment-methods",
    ),
    path(
        "user/payment-methods/<str:id>/",
        DeletePaymentMethodView.as_view(),
        name="delete-payment-method",
    ),
     path("subscription/status/", SubscriptionStatusAPIView.as_view()),
     
    # Wallet Endpoints
    path("wallet/balance/", WalletBalanceView.as_view(), name="wallet-balance"),
    path("wallet/transactions/", TransactionListView.as_view(), name="wallet-transactions"),
    path("wallet/topup/", TopUpView.as_view(), name="wallet-topup"),
    path("wallet/pay-invoice/", PayWithWalletView.as_view(), name="wallet-pay"), # Matches frontend settleInvoiceWithWallet
]

urlpatterns += router.urls
