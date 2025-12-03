# views.py
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ...models import OnboardingQuestionnaire
from ..serializers.onboarding import OnboardingQuestionnaireSerializer


class OnboardingQuestionnaireViewSet(viewsets.GenericViewSet):
    serializer_class = OnboardingQuestionnaireSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return OnboardingQuestionnaire.objects.filter(user=self.request.user)

    @action(detail=False, methods=["post"], url_path="submit")
    def submit(self, request):
        """
        User submits their onboarding questionnaire once.
        """
        obj, created = OnboardingQuestionnaire.objects.get_or_create(user=request.user)

        serializer = self.get_serializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(is_completed=True)

        return Response(serializer.data)
