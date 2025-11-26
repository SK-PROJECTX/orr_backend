from django.urls import path

from .views.account import (
    AccountSettingsView,
    ChangePasswordView,
    PasswordResetConfirmView,
    PasswordResetRequestView,
    VerifyEmailView,
    DashboardOverviewView
)
from .views.auth import LoginView, SignupView
from .views.profile import CreateOrUpdateProfileView
from .views.contact import ContactRequestView, SupportHistoryListView, SupportMessageUpdateView

urlpatterns = [
    path("verify-email/", VerifyEmailView.as_view(), name="verify-email"),
    path("register/", SignupView.as_view(), name="reqister"),
    path("login/", LoginView.as_view(), name="reqister"),
    path(
        "forget-password/",
        PasswordResetRequestView.as_view(),
        name="forget-password",
    ),
    path(
        "verify-reset-password/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="verify-reset-password",
    ),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("profile/create/", CreateOrUpdateProfileView.as_view(), name="profile-create"),
    path("account/settings/", AccountSettingsView.as_view(), name="account-settings"),
    path(
        "support/messages/",
        SupportHistoryListView.as_view(),
        name="support-messages-list",
    ),
    path(
        "support/messages/<int:message_id>/",
        SupportMessageUpdateView.as_view(),
        name="support-message-update",
    ),
    path("support", ContactRequestView.as_view(), name="support",),
    path('activities/', DashboardOverviewView.as_view(), name='activities'),
]
