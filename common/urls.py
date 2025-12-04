from django.urls import path
from .views import PublicHomepageView

from .views import CurrentUserRoleView

from .auth_views import LoginView

urlpatterns = [
    path("auth/me/", CurrentUserRoleView.as_view(), name="current-user-role"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("cms/homepage/", PublicHomepageView.as_view(), name="public-homepage"),
]
