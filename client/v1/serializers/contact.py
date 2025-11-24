from rest_framework import serializers
from ...models import ContactMessage

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ["id", "name", "email", "website", "message"]
    extra_kwargs = {
            "name": {"required": True},
            "email": {"required": True},
            "message": {"required": True},
            "website": {"required": False, "allow_null": True, "allow_blank": True},
        }