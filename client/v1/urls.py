from django.urls import path

from .views.account import (
    AccountSettingsView,
    ChangePasswordView,
    DashboardOverviewView,
    PasswordResetConfirmView,
    PasswordResetRequestView,
    VerifyEmailView,
)
from .views.admin_auth import AdminSignupView
from .views.admin_roles import AdminRolesView
from .views.auth import LoginView, SignupView
from .views.client_auth import ClientSignupView
from .views.contact import (
    ContactRequestView,
    SupportHistoryListView,
    SupportMessageUpdateView,
)
from .views.profile import CreateOrUpdateProfileView
from .views.role_check import RoleCheckView

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
    path(
        "support",
        ContactRequestView.as_view(),
        name="support",
    ),
    path("activities/", DashboardOverviewView.as_view(), name="activities"),
    path("role-check/", RoleCheckView.as_view(), name="role-check"),
    path("admin-roles/", AdminRolesView.as_view(), name="admin-roles"),
]
