from rest_framework import serializers

from ...models import ContactMessage


class CreateSupportMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ["id", "name", "email", "website", "message"]

    extra_kwargs = {
        "name": {"required": True},
        "email": {"required": True},
        "message": {"required": True},
        "website": {"required": False, "allow_null": True, "allow_blank": True},
    }


class SupportMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = [
            "id",
            "name",
            "email",
            "website",
            "message",
            "is_read",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]
