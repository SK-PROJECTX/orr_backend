from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    """Base permission for admin portal access"""
    
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            hasattr(request.user, 'admin_profile') and
            request.user.admin_profile.is_active
        )


class CanManageUsers(BasePermission):
    """Permission for user management"""
    
    def has_permission(self, request, view):
        if not (request.user.is_authenticated and hasattr(request.user, 'admin_profile')):
            return False
        
        role = request.user.admin_profile.role
        # Only super admin can manage users
        return role.name == 'super_admin' and role.can_manage_users


class CanViewAllClients(BasePermission):
    """Permission to view all clients"""
    
    def has_permission(self, request, view):
        if not (request.user.is_authenticated and hasattr(request.user, 'admin_profile')):
            return False
        
        role = request.user.admin_profile.role
        # Super admin can view all clients
        if role.name == 'super_admin':
            return True
        # Other roles need specific permission
        return role.can_view_all_clients


class CanEditClients(BasePermission):
    """Permission to edit client data"""
    
    def has_permission(self, request, view):
        if not (request.user.is_authenticated and hasattr(request.user, 'admin_profile')):
            return False
        
        role = request.user.admin_profile.role
        # Super admin can edit all clients
        if role.name == 'super_admin':
            return True
        # Admin role can edit clients if they have permission
        return role.can_edit_clients


class CanManageTickets(BasePermission):
    """Permission for ticket management"""
    
    def has_permission(self, request, view):
        if not (request.user.is_authenticated and hasattr(request.user, 'admin_profile')):
            return False
        
        role = request.user.admin_profile.role
        # Super admin, admin, and operator can manage tickets
        return role.name in ['super_admin', 'admin', 'operator'] and role.can_manage_tickets


class CanManageMeetings(BasePermission):
    """Permission for meeting management"""
    
    def has_permission(self, request, view):
        if not (request.user.is_authenticated and hasattr(request.user, 'admin_profile')):
            return False
        
        role = request.user.admin_profile.role
        # Super admin, admin, and operator can manage meetings
        return role.name in ['super_admin', 'admin', 'operator'] and role.can_manage_meetings


class CanCreateContent(BasePermission):
    """Permission to create content"""
    
    def has_permission(self, request, view):
        if not (request.user.is_authenticated and hasattr(request.user, 'admin_profile')):
            return False
        
        role = request.user.admin_profile.role
        # Super admin, admin, and content_editor can create content
        return role.name in ['super_admin', 'admin', 'content_editor'] and role.can_create_content


class CanPublishContent(BasePermission):
    """Permission to publish content"""
    
    def has_permission(self, request, view):
        if not (request.user.is_authenticated and hasattr(request.user, 'admin_profile')):
            return False
        
        role = request.user.admin_profile.role
        # Super admin and content_editor can publish content
        return role.name in ['super_admin', 'content_editor'] and role.can_publish_content


class CanViewAnalytics(BasePermission):
    """Permission to view analytics"""
    
    def has_permission(self, request, view):
        if not (request.user.is_authenticated and hasattr(request.user, 'admin_profile')):
            return False
        
        role = request.user.admin_profile.role
        # Super admin and admin can view analytics
        return role.name in ['super_admin', 'admin'] and role.can_view_analytics


class CanManageSettings(BasePermission):
    """Permission for system settings"""
    
    def has_permission(self, request, view):
        if not (request.user.is_authenticated and hasattr(request.user, 'admin_profile')):
            return False
        
        role = request.user.admin_profile.role
        # Only super admin can manage system settings
        return role.name == 'super_admin' and role.can_manage_settings


class CanViewAILogs(BasePermission):
    """Permission to view AI conversation logs"""
    
    def has_permission(self, request, view):
        if not (request.user.is_authenticated and hasattr(request.user, 'admin_profile')):
            return False
        
        role = request.user.admin_profile.role
        # Super admin and admin can view AI logs
        return role.name in ['super_admin', 'admin'] and role.can_view_ai_logs