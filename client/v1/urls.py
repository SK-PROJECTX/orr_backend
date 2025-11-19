from django.urls import include, path
from .views import VerifyEmailView, SignupView
urlpatterns = [
    path("verify-email/", VerifyEmailView.as_view(), name="verify-email"),
    path("register/", SignupView.as_view(), name="reqister"),

]