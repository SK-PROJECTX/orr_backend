from rest_framework import viewsets
from ..serializers.blog import BlogPostSerializer
from ...models import BlogPost
from django.utils import timezone

class BlogPostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BlogPost.objects.filter(published_at__lte=timezone.now())
    serializer_class = BlogPostSerializer
    lookup_field = 'slug'
    ordering_fields = ['published_at', 'title']

