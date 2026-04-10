from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from ...models import Profile
from ..serializers.profile import ProfileCreateSerializer, ProfileSerializer
from drf_spectacular.utils import extend_schema



@extend_schema(tags=["profile"])
class CreateOrUpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileCreateSerializer

    def post(self, request):
        user = request.user
        profile, created = Profile.objects.get_or_create(user=user)

        serializer = ProfileCreateSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "message": (
                    "Profile created successfully"
                    if created
                    else "Profile updated successfully"
                ),
                "profile": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


@extend_schema(tags=["profile"])
class GetProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        serializer = ProfileSerializer(profile, context={"request": request})

        return Response(
            {
                "success": True,
                "status": 200,
                "message": "Profile retrieved successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )