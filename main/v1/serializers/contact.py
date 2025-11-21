from rest_framework import serializers

from ...models import ContactMessage


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "subject",
            "message",
        ]
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
            "email": {"required": True},
            "phone": {"required": True},
            "subject": {"required": True},
            "message": {"required": True},
        }

    def validate_email(self, value):
        """Ensure email is valid and formatted properly."""
        if "@" not in value:
            raise serializers.ValidationError("Enter a valid email address.")
        return value

    def validate_message(self, value):
        """Ensure message is not empty or too short."""
        if len(value.strip()) < 5:
            raise serializers.ValidationError("Message is too short.")
        return value
