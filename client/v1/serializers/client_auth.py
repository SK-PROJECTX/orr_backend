from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class ClientSignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password", "first_name", "last_name")
    def validate(self, attrs):
        if User.objects.filter(username=attrs["username"]).exists():
            raise serializers.ValidationError("Username already exists.")

        if User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError("Email already exists.")

        return attrs