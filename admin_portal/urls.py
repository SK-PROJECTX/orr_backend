from django.urls import include, path
from .views import sync_howweoperate_it_view

urlpatterns = [
    path("v1/", include("admin_portal.v1.urls")),
    path("sync-it-translations-secret/", sync_howweoperate_it_view),
]
