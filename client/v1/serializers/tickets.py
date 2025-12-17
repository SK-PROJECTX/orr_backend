from rest_framework import serializers
from admin_portal.models import Ticket

class ClientInquiryTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            "contact_name",
            "contact_email",
            "contact_website",
            "description",
        ]

    def create(self, validated_data):
        return Ticket.objects.create(
            source="client_inquiry",
            subject="Client Inquiry",
            priority="normal",
            status="new",
            **validated_data,
        )



class TicketHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            "ticket_id",
            "subject",
            "status",
            "priority",
            "source",
            "created_at",
        ]