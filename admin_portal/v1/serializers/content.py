from rest_framework import serializers
from admin_portal.models import Content


class ContentListSerializer(serializers.ModelSerializer):
    """Content list view serializer"""
    author_name = serializers.CharField(source='author.get_full_name', allow_null=True)
    
    class Meta:
        model = Content
        fields = [
            'id', 'title', 'slug', 'summary', 'content_type', 'status',
            'stage', 'pillars', 'author_name', 'published_at', 'version',
            'view_count', 'download_count', 'created_at', 'updated_at'
        ]


class ContentDetailSerializer(serializers.ModelSerializer):
    """Detailed content view serializer"""
    author_name = serializers.CharField(source='author.get_full_name', allow_null=True)
    attachment_url = serializers.SerializerMethodField()
    attachment_size = serializers.SerializerMethodField()
    
    class Meta:
        model = Content
        fields = [
            'id', 'title', 'slug', 'summary', 'content', 'content_type', 
            'status', 'stage', 'pillars', 'attachment', 'attachment_url',
            'attachment_size', 'author_name', 'published_at', 'version',
            'view_count', 'download_count', 'created_at', 'updated_at'
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
            'title', 'slug', 'summary', 'content', 'content_type',
            'stage', 'pillars', 'attachment'
        ]
    
    def validate_slug(self, value):
        # Check for unique slug excluding current instance
        instance = getattr(self, 'instance', None)
        if Content.objects.filter(slug=value).exclude(pk=instance.pk if instance else None).exists():
            raise serializers.ValidationError("Content with this slug already exists.")
        return value


class ContentPublishSerializer(serializers.Serializer):
    """Content publish action serializer"""
    action = serializers.ChoiceField(choices=['publish', 'unpublish', 'archive'])


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