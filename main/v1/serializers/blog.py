from rest_framework import serializers
from ...models import BlogPost


class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'excerpt', 'content',
            'featured_image', 'featured_image',
            'category', 'is_featured',
            'published_at'
        ]
