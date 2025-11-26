from django.urls import path

from .views.account import (
    AccountSettingsView,
    ChangePasswordView,
    PasswordResetConfirmView,
    PasswordResetRequestView,
    VerifyEmailView,
)
from .views.auth import LoginView, SignupView
from .views.client_auth import ClientSignupView
from .views.admin_auth import AdminSignupView
from .views.profile import CreateOrUpdateProfileView
from .views.role_check import RoleCheckView
from .views.admin_roles import AdminRolesView

urlpatterns = [
    path("verify-email/", VerifyEmailView.as_view(), name="verify-email"),
    path("register/", SignupView.as_view(), name="register"),
    path("client/register/", ClientSignupView.as_view(), name="client-register"),
    path("admin-register/", AdminSignupView.as_view(), name="admin-register"),
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
    path("role-check/", RoleCheckView.as_view(), name="role-check"),
    path("admin-roles/", AdminRolesView.as_view(), name="admin-roles"),
]
