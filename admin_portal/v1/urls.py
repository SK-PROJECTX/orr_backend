from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    dashboard, client, ticket, content, meeting, analytics, notifications, ai_oversight, settings, auth, search, compliance, role_management, client_profile, system_health
)

# Authentication URLs
auth_patterns = [
    path("me/", auth.CurrentUserRoleView.as_view(), name="current-user-role"),
    path(
        "check-permission/", auth.CheckPermissionView.as_view(), name="check-permission"
    ),
]

# Dashboard URLs
dashboard_patterns = [
    path('overview/', dashboard.DashboardOverviewView.as_view(), name='dashboard-overview'),
    path('recent-activity/', dashboard.RecentActivityView.as_view(), name='dashboard-recent-activity'),
    path('quick-stats/', dashboard.QuickStatsView.as_view(), name='dashboard-quick-stats'),
    path('client-widgets/', dashboard.ClientDashboardWidgetsView.as_view(), name='dashboard-client-widgets'),
]

# Client Management URLs
client_patterns = [
    path('', client.ClientListView.as_view(), name='client-list'),
    path('<int:pk>/', client.ClientDetailView.as_view(), name='client-detail'),
    path('<int:pk>/complete-profile/', client_profile.ClientCompleteProfileView.as_view(), name='client-complete-profile'),
    path('<int:pk>/engagement-history/', client.ClientEngagementHistoryView.as_view(), name='client-engagement-history'),
    path('<int:pk>/actions/', client.ClientActionsView.as_view(), name='client-actions'),
    path('<int:client_id>/documents/', client.ClientDocumentListView.as_view(), name='client-documents'),
    path('<int:client_id>/documents/<int:pk>/', client.ClientDocumentDetailView.as_view(), name='client-document-detail'),
    path('stats/', client.ClientStatsView.as_view(), name='client-stats'),
]

# Ticket Management URLs
ticket_patterns = [
    path("", ticket.TicketListView.as_view(), name="ticket-list"),
    path("<int:pk>/", ticket.TicketDetailView.as_view(), name="ticket-detail"),
    path(
        "<int:pk>/actions/", ticket.TicketActionsView.as_view(), name="ticket-actions"
    ),
    path(
        "<int:ticket_id>/messages/",
        ticket.TicketMessagesView.as_view(),
        name="ticket-messages",
    ),
    path("my-tickets/", ticket.MyTicketsView.as_view(), name="my-tickets"),
    path("stats/", ticket.TicketStatsView.as_view(), name="ticket-stats"),
]

# Content Management URLs
content_patterns = [
    path("", content.ContentListView.as_view(), name="content-list"),
    path("<int:pk>/", content.ContentDetailView.as_view(), name="content-detail"),
    path(
        "<int:pk>/publish/",
        content.ContentPublishView.as_view(),
        name="content-publish",
    ),
    path(
        "<int:pk>/preview/",
        content.ContentPreviewView.as_view(),
        name="content-preview",
    ),
    path(
        "<int:pk>/versions/",
        content.ContentVersionsView.as_view(),
        name="content-versions",
    ),
    path(
        "bulk-actions/",
        content.ContentBulkActionsView.as_view(),
        name="content-bulk-actions",
    ),
    path("stats/", content.ContentStatsView.as_view(), name="content-stats"),
]

# Meeting Management URLs
meeting_patterns = [
    path("", meeting.MeetingListView.as_view(), name="meeting-list"),
    path("<int:pk>/", meeting.MeetingDetailView.as_view(), name="meeting-detail"),
    path(
        "<int:pk>/actions/",
        meeting.MeetingActionsView.as_view(),
        name="meeting-actions",
    ),
    path(
        "<int:pk>/assign/", meeting.MeetingAssignView.as_view(), name="meeting-assign"
    ),
    path("my-meetings/", meeting.MyMeetingsView.as_view(), name="my-meetings"),
    path("upcoming/", meeting.UpcomingMeetingsView.as_view(), name="upcoming-meetings"),
    path("stats/", meeting.MeetingStatsView.as_view(), name="meeting-stats"),
]

# Analytics URLs
analytics_patterns = [
    path(
        "overview/",
        analytics.AnalyticsOverviewView.as_view(),
        name="analytics-overview",
    ),
    path("clients/", analytics.ClientAnalyticsView.as_view(), name="client-analytics"),
    path(
        "content/", analytics.ContentAnalyticsView.as_view(), name="content-analytics"
    ),
    path("export/", analytics.ExportAnalyticsView.as_view(), name="export-analytics"),
]

# Notifications URLs
notification_patterns = [
    path("", notifications.NotificationListView.as_view(), name="notification-list"),
    path(
        "<int:pk>/",
        notifications.NotificationDetailView.as_view(),
        name="notification-detail",
    ),
    path(
        "<int:pk>/actions/",
        notifications.NotificationActionsView.as_view(),
        name="notification-actions",
    ),
    path(
        "bulk-actions/",
        notifications.NotificationBulkActionsView.as_view(),
        name="notification-bulk-actions",
    ),
    path(
        "stats/",
        notifications.NotificationStatsView.as_view(),
        name="notification-stats",
    ),
]

# AI Oversight URLs
ai_oversight_patterns = [
    path(
        "conversations/",
        ai_oversight.AIConversationListView.as_view(),
        name="ai-conversation-list",
    ),
    path(
        "conversations/<int:pk>/",
        ai_oversight.AIConversationDetailView.as_view(),
        name="ai-conversation-detail",
    ),
    path(
        "conversations/<int:pk>/actions/",
        ai_oversight.AIConversationActionsView.as_view(),
        name="ai-conversation-actions",
    ),
    path(
        "stats/",
        ai_oversight.AIConversationStatsView.as_view(),
        name="ai-conversation-stats",
    ),
]

# Settings & System Config URLs
settings_patterns = [
    path("system/", settings.SystemSettingsView.as_view(), name="system-settings"),
    path("roles/", settings.AdminRoleListView.as_view(), name="admin-role-list"),
    path(
        "roles/<int:pk>/",
        settings.AdminRoleDetailView.as_view(),
        name="admin-role-detail",
    ),
    path("users/", settings.AdminUserListView.as_view(), name="admin-user-list"),
    path(
        "users/create/",
        settings.CreateAdminUserView.as_view(),
        name="create-admin-user",
    ),
    path(
        "users/<int:pk>/",
        settings.AdminUserDetailView.as_view(),
        name="admin-user-detail",
    ),
    path(
        "users/<int:pk>/actions/",
        settings.UserManagementActionsView.as_view(),
        name="user-management-actions",
    ),
    path("audit-logs/", settings.AuditLogListView.as_view(), name="audit-log-list"),
]

# System Health URLs
system_health_patterns = [
    path('health/', system_health.SystemHealthView.as_view(), name='system-health'),
    path('performance/', system_health.SystemPerformanceView.as_view(), name='system-performance'),
]

# Search & Navigation URLs
search_patterns = [
    path("global/", search.GlobalSearchView.as_view(), name="global-search"),
    path("quick/", search.QuickSearchView.as_view(), name="quick-search"),
]

# Compliance & Data Management URLs
compliance_patterns = [
    path(
        "export-client-data/",
        compliance.ClientDataExportView.as_view(),
        name="export-client-data",
    ),
    path(
        "delete-client-data/",
        compliance.ClientDataDeletionView.as_view(),
        name="delete-client-data",
    ),
    path(
        "compliance-report/",
        compliance.ComplianceReportView.as_view(),
        name="compliance-report",
    ),
]

# Role Management URLs (Super Admin only)
role_management_patterns = [
    path('roles/<int:role_id>/permissions/', role_management.UpdateRolePermissionsView.as_view(), name='update-role-permissions'),
    path('users/<int:user_id>/deactivate/', role_management.DeactivateUserView.as_view(), name='deactivate-user'),
    path('users/<int:user_id>/edit/', role_management.EditUserView.as_view(), name='edit-user'),
]

urlpatterns = [
    path('auth/', include(auth_patterns)),
    path('dashboard/', include(dashboard_patterns)),
    path('clients/', include(client_patterns)),
    path('tickets/', include(ticket_patterns)),
    path('content/', include(content_patterns)),
    path('meetings/', include(meeting_patterns)),
    path('analytics/', include(analytics_patterns)),
    path('notifications/', include(notification_patterns)),
    path('ai-oversight/', include(ai_oversight_patterns)),
    path('settings/', include(settings_patterns)),
    path('search/', include(search_patterns)),
    path('compliance/', include(compliance_patterns)),
    path('role-management/', include(role_management_patterns)),
    path('system/', include(system_health_patterns)),
]
