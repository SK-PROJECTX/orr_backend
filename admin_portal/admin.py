from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import (
    AdminRole, AdminProfile, Client, Ticket, TicketMessage, Content, 
    Meeting, AIConversation, SystemNotification, SystemSettings, 
    AuditLog, ClientDocument
)


@admin.register(AdminRole)
class AdminRoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'can_manage_users', 'can_view_all_clients']
    list_filter = ['can_manage_users', 'can_view_all_clients', 'can_manage_tickets']
    search_fields = ['name', 'description']


@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'department', 'is_active', 'created_at']
    list_filter = ['role', 'is_active', 'department']
    search_fields = ['user__username', 'user__email', 'department']
    raw_id_fields = ['user']


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['user', 'company', 'stage', 'primary_pillar', 'assigned_admin', 'is_portal_active']
    list_filter = ['stage', 'primary_pillar', 'is_portal_active', 'assigned_admin']
    search_fields = ['user__username', 'user__email', 'company']
    raw_id_fields = ['user', 'assigned_admin']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['ticket_id', 'subject', 'client', 'status', 'priority', 'assigned_to', 'created_at']
    list_filter = ['status', 'priority', 'source', 'assigned_to']
    search_fields = ['ticket_id', 'subject', 'client__user__email', 'client__company']
    raw_id_fields = ['client', 'assigned_to', 'related_meeting', 'related_content']
    readonly_fields = ['ticket_id', 'created_at', 'updated_at']


@admin.register(TicketMessage)
class TicketMessageAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'sender', 'is_internal', 'created_at']
    list_filter = ['is_internal', 'created_at']
    search_fields = ['ticket__ticket_id', 'sender__username', 'message']
    raw_id_fields = ['ticket', 'sender']


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ['title', 'content_type', 'status', 'stage', 'author', 'published_at']
    list_filter = ['content_type', 'status', 'stage', 'author']
    search_fields = ['title', 'summary', 'content']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    readonly_fields = ['view_count', 'download_count', 'created_at', 'updated_at']


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ['client', 'meeting_type', 'status', 'requested_datetime', 'host']
    list_filter = ['meeting_type', 'status', 'host']
    search_fields = ['client__user__email', 'client__company', 'agenda']
    raw_id_fields = ['client', 'host']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(AIConversation)
class AIConversationAdmin(admin.ModelAdmin):
    list_display = ['client', 'session_id', 'escalated_to_ticket', 'needs_improvement', 'created_at']
    list_filter = ['escalated_to_ticket', 'needs_improvement', 'reviewed_by']
    search_fields = ['client__user__email', 'session_id', 'summary']
    raw_id_fields = ['client', 'reviewed_by']


@admin.register(SystemNotification)
class SystemNotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'notification_type', 'recipient', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['title', 'message', 'recipient__username']
    raw_id_fields = ['recipient', 'related_ticket', 'related_meeting', 'related_client']


@admin.register(SystemSettings)
class SystemSettingsAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'primary_color', 'email_notifications_enabled']
    
    def has_add_permission(self, request):
        # Only allow one SystemSettings instance
        return not SystemSettings.objects.exists()


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'model_name', 'description', 'timestamp']
    list_filter = ['action', 'model_name', 'timestamp']
    search_fields = ['user__username', 'description', 'model_name']
    readonly_fields = ['timestamp']
    raw_id_fields = ['user']


@admin.register(ClientDocument)
class ClientDocumentAdmin(admin.ModelAdmin):
    list_display = ['client', 'title', 'document_type', 'is_visible_to_client', 'uploaded_by', 'created_at']
    list_filter = ['document_type', 'is_visible_to_client', 'uploaded_by']
    search_fields = ['client__user__email', 'title', 'description']
    raw_id_fields = ['client', 'uploaded_by']