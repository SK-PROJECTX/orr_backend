from django.urls import path
from .views import VerifyEmailView, SignupView, LoginView
urlpatterns = [
    path("verify-email/", VerifyEmailView.as_view(), name="verify-email"),
    path("register/", SignupView.as_view(), name="reqister"),
     path("login/", LoginView.as_view(), name="reqister"),

]