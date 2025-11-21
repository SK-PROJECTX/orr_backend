from rest_framework import serializers

from ...models import Profile


class ProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "full_name",
            "nickname",
            "gender",
            "country",
            "language",
            "timezone",
        ]
