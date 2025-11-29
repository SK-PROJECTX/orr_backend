from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import IsClientOrAdmin
from .serializers import UserRoleSerializer


@extend_schema(
    tags=["Authentication"],
    summary="Get current user role and permissions",
    description="Retrieve the current user's role, permissions, and profile information.",
)
class CurrentUserRoleView(APIView):
    """Get current user role and permissions"""

    permission_classes = [IsClientOrAdmin]

    def get(self, request):
        serializer = UserRoleSerializer(request.user)
        return Response(serializer.data)
