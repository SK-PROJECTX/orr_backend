from django.urls import path, include
from .views import BlogPostViewSet
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'blogs', BlogPostViewSet)


urlpatterns = [
    path('', include(router.urls)),
]