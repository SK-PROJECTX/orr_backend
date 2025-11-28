from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    """Base permission for admin portal access"""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and hasattr(request.user, "admin_profile")
            and request.user.admin_profile.is_active
        )


class CanManageUsers(BasePermission):
    """Permission for user management"""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and hasattr(request.user, "admin_profile")
            and request.user.admin_profile.role.can_manage_users
        )


class CanViewAllClients(BasePermission):
    """Permission to view all clients"""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and hasattr(request.user, "admin_profile")
            and request.user.admin_profile.role.can_view_all_clients
        )


class CanEditClients(BasePermission):
    """Permission to edit client data"""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and hasattr(request.user, "admin_profile")
            and request.user.admin_profile.role.can_edit_clients
        )


class CanManageTickets(BasePermission):
    """Permission for ticket management"""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and hasattr(request.user, "admin_profile")
            and request.user.admin_profile.role.can_manage_tickets
        )


class CanManageMeetings(BasePermission):
    """Permission for meeting management"""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and hasattr(request.user, "admin_profile")
            and request.user.admin_profile.role.can_manage_meetings
        )


class CanCreateContent(BasePermission):
    """Permission to create content"""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and hasattr(request.user, "admin_profile")
            and request.user.admin_profile.role.can_create_content
        )


class CanPublishContent(BasePermission):
    """Permission to publish content"""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and hasattr(request.user, "admin_profile")
            and request.user.admin_profile.role.can_publish_content
        )


class CanViewAnalytics(BasePermission):
    """Permission to view analytics"""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and hasattr(request.user, "admin_profile")
            and request.user.admin_profile.role.can_view_analytics
        )


class CanManageSettings(BasePermission):
    """Permission for system settings"""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and hasattr(request.user, "admin_profile")
            and request.user.admin_profile.role.can_manage_settings
        )


class CanViewAILogs(BasePermission):
    """Permission to view AI conversation logs"""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and hasattr(request.user, "admin_profile")
            and request.user.admin_profile.role.can_view_ai_logs
        )


class IsAdminExceptContentEditor(BasePermission):
    """
    Allows access ONLY to authenticated admin users
    EXCEPT those with the 'content_editor' role.
    """

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False
        if not hasattr(user, "admin_profile"):
            return False

        profile = user.admin_profile
        if not profile.is_active:
            return False

        if profile.role and profile.role.name == "content_editor":
            return False

        return True