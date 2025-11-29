from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from admin_portal.permissions import IsAdminUser


@extend_schema(
    tags=["Authentication"],
    summary="Get current user role and permissions",
    description="Retrieve the current authenticated user's role, permissions, and access levels for the admin portal.",
)
class CurrentUserRoleView(APIView):
    """Get current user's role and permissions"""

    permission_classes = [IsAdminUser]

    def get(self, request):
        user = request.user
        admin_profile = user.admin_profile
        role = admin_profile.role

        return Response(
            {
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "full_name": user.get_full_name(),
                    "is_superuser": user.is_superuser,
                },
                "profile": {
                    "id": admin_profile.id,
                    "department": admin_profile.department,
                    "phone": admin_profile.phone,
                    "is_active": admin_profile.is_active,
                },
                "role": {
                    "id": role.id,
                    "name": role.name,
                    "display_name": role.get_name_display(),
                    "description": role.description,
                },
                "permissions": {
                    "can_manage_users": role.can_manage_users,
                    "can_view_all_clients": role.can_view_all_clients,
                    "can_edit_clients": role.can_edit_clients,
                    "can_manage_tickets": role.can_manage_tickets,
                    "can_manage_meetings": role.can_manage_meetings,
                    "can_create_content": role.can_create_content,
                    "can_publish_content": role.can_publish_content,
                    "can_view_analytics": role.can_view_analytics,
                    "can_view_billing": role.can_view_billing,
                    "can_manage_settings": role.can_manage_settings,
                    "can_view_ai_logs": role.can_view_ai_logs,
                },
            }
        )


@extend_schema(
    tags=["Authentication"],
    summary="Check specific permission",
    description="Check if the current user has a specific permission for conditional UI rendering.",
)
class CheckPermissionView(APIView):
    """Check if user has specific permission"""

    permission_classes = [IsAdminUser]

    def post(self, request):
        permission = request.data.get("permission")
        user = request.user

        if not hasattr(user, "admin_profile"):
            return Response({"has_permission": False})

        role = user.admin_profile.role

        # Map permission names to role attributes
        permission_map = {
            "manage_users": role.can_manage_users,
            "view_all_clients": role.can_view_all_clients,
            "edit_clients": role.can_edit_clients,
            "manage_tickets": role.can_manage_tickets,
            "manage_meetings": role.can_manage_meetings,
            "create_content": role.can_create_content,
            "publish_content": role.can_publish_content,
            "view_analytics": role.can_view_analytics,
            "view_billing": role.can_view_billing,
            "manage_settings": role.can_manage_settings,
            "view_ai_logs": role.can_view_ai_logs,
        }

        has_permission = permission_map.get(permission, False)

        return Response({"permission": permission, "has_permission": has_permission})
