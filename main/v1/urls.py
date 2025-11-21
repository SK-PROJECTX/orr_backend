from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views.blog import BlogPostViewSet
from .views.contact import ContactMessageView

router = DefaultRouter()
router.register(r"blogs", BlogPostViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("contact/", ContactMessageView.as_view()),
]
