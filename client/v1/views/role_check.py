from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema


@extend_schema(
    tags=["Authentication"],
    summary="Check user role and redirect",
    description="Check if user is client or admin and return appropriate redirect URL."
)
class RoleCheckView(APIView):
    """Check user role for frontend routing"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        if hasattr(user, 'admin_profile') and user.admin_profile.is_active:
            return Response({
                'user_type': 'admin',
                'redirect_url': '/admin-portal/dashboard/',
                'role': user.admin_profile.role.name if user.admin_profile.role else None
            })
        elif hasattr(user, 'client_profile'):
            return Response({
                'user_type': 'client', 
                'redirect_url': '/client-portal/dashboard/',
                'active': user.client_profile.is_portal_active
            })
        else:
            return Response({
                'user_type': 'unknown',
                'redirect_url': '/login/',
                'error': 'No valid profile found'
            })