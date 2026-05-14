from django.contrib.auth.models import User
from rest_framework import serializers


class UserRoleSerializer(serializers.ModelSerializer):
    """Serializer for user with role information"""

    user_type = serializers.SerializerMethodField()
    role_details = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()
    client_id = serializers.SerializerMethodField()
    admin_id = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "user_type",
            "role_details",
            "permissions",
            "client_id",
            "admin_id",
        ]

    def get_client_id(self, obj):
        if hasattr(obj, 'client_profile'):
            return obj.client_profile.id
        return None

    def get_admin_id(self, obj):
        if hasattr(obj, 'admin_profile'):
            return obj.admin_profile.id
        return None

    def get_user_type(self, obj):
        """Determine if user is client or admin"""
        if hasattr(obj, "admin_profile"):
            return "admin"
        elif hasattr(obj, "profile"):
            return "client"
        return "unknown"

    def get_role_details(self, obj):
        """Get role-specific details"""
        if hasattr(obj, "admin_profile") and obj.admin_profile.role:
            return {
                "role_name": obj.admin_profile.role.name,
                "role_display": obj.admin_profile.role.get_name_display(),
                "department": obj.admin_profile.department,
            }
        elif hasattr(obj, "profile"):
            return {
                "full_name": obj.profile.full_name,
                "country": obj.profile.country,
                "city": obj.profile.city,
            }
        return None

    def get_permissions(self, obj):
        """Get user permissions"""
        if hasattr(obj, "admin_profile") and obj.admin_profile.role:
            role = obj.admin_profile.role
            return {
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
            }
        elif hasattr(obj, "profile"):
            return {
                "can_access_portal": True,
                "can_request_meetings": True,
                "can_create_tickets": True,
                "can_view_resources": True,
            }
        return {}
