from rest_framework import serializers
from ...models import FavoriteDocument


class FavoriteDocumentSerializer(serializers.ModelSerializer):
    document_title = serializers.CharField(source="document.title", read_only=True)
    document_file = serializers.FileField(source="document.document", read_only=True)

    class Meta:
        model = FavoriteDocument
        fields = ["id", "document", "document_title", "document_file", "created_at"]