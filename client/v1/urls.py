from django.urls import path

from .views.account import (
    AccountSettingsView,
    ChangePasswordView,
    PasswordResetConfirmView,
    PasswordResetRequestView,
    VerifyEmailView,
)
from .views.auth import LoginView, SignupView
from .views.profile import CreateOrUpdateProfileView

urlpatterns = [
    path("verify-email/", VerifyEmailView.as_view(), name="verify-email"),
    path("register/", SignupView.as_view(), name="reqister"),
    path("login/", LoginView.as_view(), name="reqister"),
    path(
        "reset-password/",
        PasswordResetRequestView.as_view(),
        name="reset-password",
    ),
    path(
        "verify-reset-password/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="verify-reset-password",
    ),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("profile/create/", CreateOrUpdateProfileView.as_view(), name="profile-create"),
    path("account/settings/", AccountSettingsView.as_view(), name="account-settings"),
]
