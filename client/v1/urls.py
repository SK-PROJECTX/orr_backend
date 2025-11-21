from django.urls import path
from .views import VerifyEmailView, SignupView, LoginView, PasswordResetRequestView, PasswordResetConfirmView, ChangePasswordView
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
]