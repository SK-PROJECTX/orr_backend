from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ...models import Profile
from ..serializers.profile import ProfileCreateSerializer


class CreateOrUpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]

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
