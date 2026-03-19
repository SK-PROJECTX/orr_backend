# serializers.py
from rest_framework import serializers

from ...models import OnboardingQuestionnaire


class OnboardingQuestionnaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnboardingQuestionnaire
        fields = "__all__"
        read_only_fields = ["user", "created_at", "updated_at"]

    def validate(self, data):
        if not data.get("accepted_service_agreement", False):
            raise serializers.ValidationError(
                {
                    "accepted_service_agreement": "You must accept the Service Agreement to continue."
                }
            )

        if (
            data.get("jurisdiction") == "other"
            and not data.get("jurisdiction_other", "").strip()
        ):
            raise serializers.ValidationError(
                {
                    "jurisdiction_other": "This field is required when 'Other' is selected."
                }
            )

        return data

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        validated_data["is_completed"] = True
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.is_completed = True
        return super().update(instance, validated_data)

class OnboardingStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnboardingQuestionnaire
        fields = ["is_completed"] 