from django.urls import path, include
from .views.blog import BlogPostViewSet
from .views.contact import ContactMessageView
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'blogs', BlogPostViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path("contact/", ContactMessageView.as_view()),
]