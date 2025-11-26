from rest_framework import serializers


class SearchResultSerializer(serializers.Serializer):
    """Serializer for search results"""
    query = serializers.CharField()
    results = serializers.DictField()
    total_count = serializers.IntegerField()


class QuickSearchSuggestionSerializer(serializers.Serializer):
    """Serializer for quick search suggestions"""
    type = serializers.CharField()
    id = serializers.IntegerField()
    title = serializers.CharField()
    url = serializers.CharField()


class QuickSearchResponseSerializer(serializers.Serializer):
    """Serializer for quick search response"""
    suggestions = QuickSearchSuggestionSerializer(many=True)