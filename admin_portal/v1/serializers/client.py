import time
from django.contrib.auth.models import User
from rest_framework import serializers

from admin_portal.models import Client, ClientDocument, Meeting, Ticket


class ClientListSerializer(serializers.ModelSerializer):
    """Client list view serializer"""

    full_name = serializers.SerializerMethodField()
    email = serializers.CharField(source="user.email")
    username = serializers.CharField(source="user.username")
    assigned_admin_name = serializers.SerializerMethodField()

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
            "is_portal_active",
            "last_activity",
            "created_at",
        ]
    
    def get_full_name(self, obj):
        full_name = obj.user.get_full_name().strip()
        if full_name:
            return full_name
        return obj.user.username or "Unknown User"
    
    def get_assigned_admin_name(self, obj):
        if not obj.assigned_admin:
            return None
        full_name = obj.assigned_admin.get_full_name().strip()
        if full_name:
            return full_name
        return obj.assigned_admin.username or "Unknown Admin"


class ClientDetailSerializer(serializers.ModelSerializer):
    """Detailed client view serializer"""

    full_name = serializers.SerializerMethodField()
    email = serializers.CharField(source="user.email")
    username = serializers.CharField(source="user.username")
    date_joined = serializers.DateTimeField(source="user.date_joined")
    last_login = serializers.DateTimeField(source="user.last_login")
    assigned_admin_name = serializers.SerializerMethodField()

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
        try:
            return obj.tickets.count()
        except Exception:
            return 0

    def get_meetings_count(self, obj):
        try:
            return obj.meetings.count()
        except Exception:
            return 0

    def get_documents_count(self, obj):
        try:
            return obj.documents.count()
        except Exception:
            return 0
    
    def get_full_name(self, obj):
        full_name = obj.user.get_full_name().strip()
        if full_name:
            return full_name
        return obj.user.username or "Unknown User"
    
    def get_assigned_admin_name(self, obj):
        if not obj.assigned_admin:
            return None
        full_name = obj.assigned_admin.get_full_name().strip()
        if full_name:
            return full_name
        return obj.assigned_admin.username or "Unknown Admin"


class ClientCreateSerializer(serializers.ModelSerializer):
    """Client creation serializer"""
    
    username = serializers.CharField(write_only=True, required=False, allow_blank=True)
    email = serializers.EmailField(write_only=True)
    full_name = serializers.CharField(write_only=True, required=False, allow_blank=True)
    secondary_pillars = serializers.CharField(write_only=True, required=False, allow_blank=True)
    internal_notes = serializers.CharField(write_only=True, required=False, allow_blank=True)
    
    class Meta:
        model = Client
        fields = [
            "username",
            "email",
            "full_name",
            "company",
            "role",
            "stage",
            "primary_pillar",
            "secondary_pillars",
            "internal_notes",
        ]
        extra_kwargs = {
            'stage': {'required': False},
            'primary_pillar': {'required': False},
            'role': {'required': False},
            'company': {'required': True},
            'secondary_pillars': {'required': False},
            'internal_notes': {'required': False},
        }
        
    def validate_email(self, value):
        """Validate email - allow existing emails for now, handle in view"""
        if not value or not value.strip():
            raise serializers.ValidationError("Email is required")
        return value.strip().lower()
        
    def validate_company(self, value):
        """Validate company name"""
        if not value or not value.strip():
            raise serializers.ValidationError("Company name is required")
        return value.strip()
        
    def validate(self, attrs):
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"Validating client data: {attrs}")
        
        # Ensure email is provided
        if not attrs.get('email'):
            raise serializers.ValidationError("Email is required")
            
        # Ensure company is provided
        if not attrs.get('company'):
            raise serializers.ValidationError("Company name is required")
        
        logger.info(f"Final validated data: {attrs}")
        return attrs


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

    uploaded_by_name = serializers.SerializerMethodField()
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
    
    def get_uploaded_by_name(self, obj):
        if not obj.uploaded_by:
            return "Unknown User"
        full_name = obj.uploaded_by.get_full_name().strip()
        if full_name:
            return full_name
        return obj.uploaded_by.username or "Unknown User"


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
