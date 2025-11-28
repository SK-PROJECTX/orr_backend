from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from .serializers import UserRoleSerializer
from .permissions import IsClientOrAdmin


@extend_schema(
    tags=["Authentication"],
    summary="Get current user role and permissions",
    description="Retrieve the current user's role, permissions, and profile information."
)
class CurrentUserRoleView(APIView):
    """Get current user role and permissions"""
    permission_classes = [IsClientOrAdmin]
    
    def get(self, request):
        serializer = UserRoleSerializer(request.user)
        return Response(serializer.data)