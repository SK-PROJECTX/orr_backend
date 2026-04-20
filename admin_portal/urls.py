from django.urls import include, path
from .views import sync_cms_it_view

urlpatterns = [
    path("v1/", include("admin_portal.v1.urls")),
    path("sync-it-translations-secret/", sync_cms_it_view),
]
