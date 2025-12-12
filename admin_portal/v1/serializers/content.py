from rest_framework import serializers

from admin_portal.models import Content


class ContentListSerializer(serializers.ModelSerializer):
    """Content list view serializer"""

    author_name = serializers.CharField(source="author.get_full_name", allow_null=True)

    class Meta:
        model = Content
        fields = [
            "id",
            "title",
            "slug",
            "summary",
            "content_type",
            "status",
            "stage",
            "pillars",
            "author_name",
            "published_at",
            "version",
            "view_count",
            "download_count",
            "created_at",
            "updated_at",
        ]


class ContentDetailSerializer(serializers.ModelSerializer):
    """Detailed content view serializer"""

    author_name = serializers.CharField(source="author.get_full_name", allow_null=True)
    attachment_url = serializers.SerializerMethodField()
    attachment_size = serializers.SerializerMethodField()

    class Meta:
        model = Content
        fields = [
            "id",
            "title",
            "slug",
            "summary",
            "content",
            "content_type",
            "status",
            "stage",
            "pillars",
            "attachment",
            "attachment_url",
            "attachment_size",
            "author_name",
            "published_at",
            "version",
            "view_count",
            "download_count",
            "created_at",
            "updated_at",
        ]

    def get_attachment_url(self, obj):
        if obj.attachment:
            return obj.attachment.url
        return None

    def get_attachment_size(self, obj):
        if obj.attachment:
            return obj.attachment.size
        return 0


class ContentCreateUpdateSerializer(serializers.ModelSerializer):
    """Content create/update serializer"""

    class Meta:
        model = Content
        fields = [
            "title",
            "slug",
            "summary",
            "content",
            "content_type",
            "status",
            "stage",
            "pillars",
            "attachment",
        ]
        extra_kwargs = {
            'slug': {'required': False}
        }

    def validate(self, data):
        # Auto-generate slug if not provided
        if not data.get('slug') and data.get('title'):
            from django.utils.text import slugify
            data['slug'] = slugify(data['title'])
        
        # Check for unique slug excluding current instance
        slug = data.get('slug')
        if slug:
            instance = getattr(self, "instance", None)
            if (
                Content.objects.filter(slug=slug)
                .exclude(pk=instance.pk if instance else None)
                .exists()
            ):
                # Auto-append number to make it unique
                base_slug = slug
                counter = 1
                while Content.objects.filter(slug=slug).exclude(pk=instance.pk if instance else None).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                data['slug'] = slug
        
        return data
        
    def validate_pillars(self, value):
        # Convert single pillar string to list for consistency
        if isinstance(value, str):
            return [value]
        return value


class ContentPublishSerializer(serializers.Serializer):
    """Content publish action serializer"""

    action = serializers.ChoiceField(choices=["publish", "unpublish", "archive"])


class ContentStatsSerializer(serializers.Serializer):
    """Content statistics serializer"""

    total_content = serializers.IntegerField()
    published_content = serializers.IntegerField()
    draft_content = serializers.IntegerField()
    archived_content = serializers.IntegerField()
    content_by_type = serializers.DictField()
    content_by_stage = serializers.DictField()
    content_by_pillar = serializers.DictField()
    most_viewed = serializers.ListField()
    most_downloaded = serializers.ListField()
