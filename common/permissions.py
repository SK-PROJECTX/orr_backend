from rest_framework.permissions import BasePermission


class IsClientUser(BasePermission):
    """Permission for client portal users"""
    
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            hasattr(request.user, 'profile')
        )


class IsAdminUser(BasePermission):
    """Permission for admin portal users"""
    
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            hasattr(request.user, 'admin_profile') and
            request.user.admin_profile.is_active
        )


class IsClientOrAdmin(BasePermission):
    """Permission for both client and admin users"""
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        return (
            hasattr(request.user, 'profile') or
            (hasattr(request.user, 'admin_profile') and request.user.admin_profile.is_active)
        )