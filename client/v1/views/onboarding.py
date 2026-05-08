# views.py
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ...models import OnboardingQuestionnaire
from ..serializers.onboarding import OnboardingQuestionnaireSerializer, OnboardingStatusSerializer

class OnboardingQuestionnaireViewSet(viewsets.GenericViewSet):
    serializer_class = OnboardingQuestionnaireSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return OnboardingQuestionnaire.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=["get"], url_path="me")
    def me(self, request):
        """
        Called on login / app reload.
        Always returns the onboarding object with its is_completed status.
        """
        obj, created = OnboardingQuestionnaire.objects.get_or_create(
            user=request.user,
            defaults={"is_completed": False},
        )

        serializer = self.get_serializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    @action(detail=False, methods=["get"], url_path="status")
    def onboarding_status(self, request):
        """
        Returns onboarding status (is_completed) only.
        Uses a different serializer.
        """
        obj, _ = OnboardingQuestionnaire.objects.get_or_create(
            user=request.user,
            defaults={"is_completed": False},
        )

        serializer = OnboardingStatusSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    @action(detail=False, methods=["post"], url_path="submit")
    def submit(self, request):
        """
        User submits their onboarding questionnaire once.
        """
        obj, created = OnboardingQuestionnaire.objects.get_or_create(user=request.user)

        serializer = self.get_serializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        onboarding = serializer.save(is_completed=True)

        # Sync relevant data to Client record (admin portal)
        from admin_portal.models import Client
        client, _ = Client.objects.get_or_create(user=request.user)
        
        # Update client company if it's still default or empty
        if client.company in ["N/A", "", None]:
            if onboarding.jurisdiction == 'malta':
                client.company = f"Malta Business ({request.user.username})"
            elif onboarding.jurisdiction_other:
                client.company = f"{onboarding.jurisdiction_other} Business ({request.user.username})"
            else:
                client.company = f"Project {request.user.username}"
        
        # Sync pillars
        if onboarding.orr_pillars:
            pillars = onboarding.orr_pillars
            if isinstance(pillars, str):
                pillars = [p.strip().lower() for p in pillars.split(',') if p.strip()]
            
            if pillars:
                # Map first pillar to primary_pillar if it matches choices
                pillar_map = {
                    'strategic': 'strategic',
                    'operational': 'operational',
                    'financial': 'financial',
                    'cultural': 'cultural'
                }
                
                valid_pillars = [pillar_map.get(p.lower()) for p in pillars if p.lower() in pillar_map]
                if valid_pillars:
                    client.primary_pillar = valid_pillars[0]
                    client.secondary_pillars = valid_pillars[1:]
        
        client.save()

        return Response(serializer.data)
    
