from django.contrib.auth.models import User
from rest_framework import serializers

from admin_portal.models import Client, ClientDocument, Meeting, Ticket


class ClientListSerializer(serializers.ModelSerializer):
    """Client list view serializer"""

    full_name = serializers.CharField(source="user.get_full_name")
    email = serializers.CharField(source="user.email")
    assigned_admin_name = serializers.CharField(
        source="assigned_admin.get_full_name", allow_null=True
    )

    class Meta:
        model = Client
        fields = [
            "id",
            "full_name",
            "email",
            "company",
            "role",
            "stage",
            "primary_pillar",
            "assigned_admin_name",
            "is_portal_active",
            "last_activity",
            "created_at",
        ]


class ClientDetailSerializer(serializers.ModelSerializer):
    """Detailed client view serializer"""

    full_name = serializers.CharField(source="user.get_full_name")
    email = serializers.CharField(source="user.email")
    username = serializers.CharField(source="user.username")
    date_joined = serializers.DateTimeField(source="user.date_joined")
    last_login = serializers.DateTimeField(source="user.last_login")
    assigned_admin_name = serializers.CharField(
        source="assigned_admin.get_full_name", allow_null=True
    )

    # Related data counts
    tickets_count = serializers.SerializerMethodField()
    meetings_count = serializers.SerializerMethodField()
    documents_count = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = [
            "id",
            "full_name",
            "email",
            "username",
            "company",
            "role",
            "stage",
            "primary_pillar",
            "secondary_pillars",
            "assigned_admin_name",
            "internal_notes",
            "is_portal_active",
            "last_activity",
            "date_joined",
            "last_login",
            "created_at",
            "updated_at",
            "tickets_count",
            "meetings_count",
            "documents_count",
        ]

    def get_tickets_count(self, obj):
        return obj.tickets.count()

    def get_meetings_count(self, obj):
        return obj.meetings.count()

    def get_documents_count(self, obj):
        return obj.documents.count()


class ClientUpdateSerializer(serializers.ModelSerializer):
    """Client update serializer"""

    class Meta:
        model = Client
        fields = [
            "company",
            "role",
            "stage",
            "primary_pillar",
            "secondary_pillars",
            "assigned_admin",
            "internal_notes",
            "is_portal_active",
        ]


class ClientDocumentSerializer(serializers.ModelSerializer):
    """Client document serializer"""

    uploaded_by_name = serializers.CharField(
        source="uploaded_by.get_full_name", read_only=True
    )
    file_size = serializers.SerializerMethodField()

    class Meta:
        model = ClientDocument
        fields = [
            "id",
            "title",
            "description",
            "document",
            "document_type",
            "is_visible_to_client",
            "uploaded_by_name",
            "download_count",
            "last_accessed",
            "created_at",
            "file_size",
        ]

    def get_file_size(self, obj):
        if obj.document:
            return obj.document.size
        return 0


class ClientEngagementHistorySerializer(serializers.Serializer):
    """Client engagement history"""

    tickets = serializers.SerializerMethodField()
    meetings = serializers.SerializerMethodField()
    documents = serializers.SerializerMethodField()

    def get_tickets(self, obj):
        from .ticket import TicketListSerializer

        tickets = obj.tickets.all()[:5]  # Latest 5
        return TicketListSerializer(tickets, many=True).data

    def get_meetings(self, obj):
        from .meeting import MeetingListSerializer

        meetings = obj.meetings.all()[:5]  # Latest 5
        return MeetingListSerializer(meetings, many=True).data

    def get_documents(self, obj):
        documents = obj.documents.all()[:5]  # Latest 5
        return ClientDocumentSerializer(documents, many=True).data
