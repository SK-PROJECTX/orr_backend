from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views.document import ClientDocumentsView

from .views.tickets import ClientTicketCreateAPIView, ClientTicketHistoryAPIView
from .views.account import (
    AccountSettingsView,
    ChangePasswordView,
    DashboardOverviewView,
    PasswordResetConfirmView,
    PasswordResetRequestView,
    VerifyEmailView,
)
from .views.favourite import FavoriteDeleteView, FavoriteListView, ToggleFavoriteView
from .views.admin_auth import AdminSignupView
from .views.admin_roles import AdminRolesView
from .views.auth import LoginView, SignupView
from .views.client_auth import ClientSignupView
from .views.onboarding import OnboardingQuestionnaireViewSet
from .views.profile import CreateOrUpdateProfileView, GetProfileView
from .views.role_check import RoleCheckView

router = DefaultRouter()
router.register(r"onboarding", OnboardingQuestionnaireViewSet, basename="onboarding")


urlpatterns = [
    path("", include(router.urls)),
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
    path("activities/", DashboardOverviewView.as_view(), name="activities"),
    path("role-check/", RoleCheckView.as_view(), name="role-check"),
    path("admin-roles/", AdminRolesView.as_view(), name="admin-roles"),
    path("favorites/", FavoriteListView.as_view(), name="favorites-list"),
    path("favorites/<int:document_id>/toggle/", ToggleFavoriteView.as_view(), name="favorites-toggle"),
    path("favorites/<int:pk>/delete/", FavoriteDeleteView.as_view(), name="favorites-delete"),
     path("client/documents/", ClientDocumentsView.as_view(), name="client-documents"),
    path("profile/", GetProfileView.as_view(), name="get-profile"),
    path(
        "tickets/create/",
        ClientTicketCreateAPIView.as_view(),
        name="ticket-create",
    ),
    path(
        "tickets/history/",
        ClientTicketHistoryAPIView.as_view(),
        name="ticket-history",
    ),
]
