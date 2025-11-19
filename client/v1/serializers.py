from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("username", "email", "password")

class VerifyEmailSerializer(serializers.Serializer):
    uid = serializers.CharField(help_text="User UID from email")
    token = serializers.CharField(help_text="Email verification token")

class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        identifier = attrs.get("identifier")
        password = attrs.get("password")

        if not identifier or not password:
            raise serializers.ValidationError(
                "Identifier (email or username) and password are required."
            )

        User = get_user_model()
        user = (
            User.objects.filter(username__iexact=identifier).first()
            or User.objects.filter(email__iexact=identifier).first()
        )

        if not user:
            raise serializers.ValidationError("Invalid login credentials.")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid login credentials.")

        attrs["user"] = user
        return attrs