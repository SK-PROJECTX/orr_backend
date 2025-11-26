from django.urls import path
from .views import CurrentUserRoleView

urlpatterns = [
    path('auth/me/', CurrentUserRoleView.as_view(), name='current-user-role'),
]