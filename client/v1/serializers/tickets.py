from rest_framework import serializers
from admin_portal.models import Ticket, TicketMessage

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
        description = validated_data.get('description', '')
        # Generate subject from description (first 50 chars)
        subject = description[:50] + '...' if len(description) > 50 else description
        if not subject:
            subject = "Client Inquiry"

        ticket = Ticket.objects.create(
            source="client_inquiry",
            subject=subject,
            priority="normal",
            status="new",
            **validated_data,
        )

        # Create initial message from client
        request = self.context.get('request')
        if request and request.user:
            TicketMessage.objects.create(
                ticket=ticket,
                sender=request.user,
                message=description,
                is_internal=False
            )
        
        return ticket



class TicketHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            "id",
            "ticket_id",
            "subject",
            "status",
            "priority",
            "source",
            "created_at",
        ]