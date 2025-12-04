from rest_framework import serializers

from admin_portal.models import Ticket, TicketMessage


class TicketListSerializer(serializers.ModelSerializer):
    """Payment ticket list view serializer"""

    client_name = serializers.CharField(source="client.user.get_full_name")
    client_company = serializers.CharField(source="client.company")
    assigned_to_name = serializers.CharField(
        source="assigned_to.get_full_name", allow_null=True
    )
    messages_count = serializers.SerializerMethodField()
    payment_type = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = [
            "id",
            "ticket_id",
            "subject",
            "status",
            "priority",
            "source",
            "client_name",
            "client_company",
            "assigned_to_name",
            "messages_count",
            "payment_type",
            "payment_amount",
            "refund_amount",
            "stripe_payment_intent_id",
            "created_at",
            "updated_at",
        ]

    def get_messages_count(self, obj):
        return obj.messages.count()
        
    def get_payment_type(self, obj):
        if obj.related_invoice:
            return "invoice"
        elif obj.related_subscription:
            return "subscription"
        return "unknown"


class TicketDetailSerializer(serializers.ModelSerializer):
    """Detailed payment ticket view serializer"""

    client_name = serializers.CharField(source="client.user.get_full_name")
    client_email = serializers.CharField(source="client.user.email")
    client_company = serializers.CharField(source="client.company")
    assigned_to_name = serializers.CharField(
        source="assigned_to.get_full_name", allow_null=True
    )
    related_payment_info = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = [
            "id",
            "ticket_id",
            "subject",
            "description",
            "status",
            "priority",
            "source",
            "client_name",
            "client_email",
            "client_company",
            "assigned_to_name",
            "internal_notes",
            "payment_amount",
            "refund_amount",
            "stripe_payment_intent_id",
            "related_payment_info",
            "created_at",
            "updated_at",
        ]

    def get_related_payment_info(self, obj):
        if obj.related_invoice:
            return {
                "type": "invoice",
                "id": obj.related_invoice.id,
                "stripe_id": obj.related_invoice.stripe_invoice_id,
                "amount": obj.related_invoice.amount,
                "status": obj.related_invoice.status,
                "billing_date": obj.related_invoice.billing_date,
            }
        elif obj.related_subscription:
            return {
                "type": "subscription",
                "id": obj.related_subscription.id,
                "stripe_id": obj.related_subscription.stripe_subscription_id,
                "plan_name": obj.related_subscription.plan_name,
                "is_active": obj.related_subscription.is_active,
                "current_period_end": obj.related_subscription.current_period_end,
            }
        return None


class TicketUpdateSerializer(serializers.ModelSerializer):
    """Payment ticket update serializer"""

    class Meta:
        model = Ticket
        fields = [
            "status",
            "priority",
            "assigned_to",
            "internal_notes",
            "related_invoice",
            "related_subscription",
            "payment_amount",
            "refund_amount",
            "stripe_payment_intent_id",
        ]


class TicketMessageSerializer(serializers.ModelSerializer):
    """Ticket message serializer"""

    sender_name = serializers.CharField(source="sender.get_full_name")
    sender_type = serializers.SerializerMethodField()

    class Meta:
        model = TicketMessage
        fields = [
            "id",
            "message",
            "sender_name",
            "sender_type",
            "is_internal",
            "created_at",
        ]

    def get_sender_type(self, obj):
        # Determine if sender is admin or client
        if hasattr(obj.sender, "admin_profile"):
            return "admin"
        return "client"


class TicketCreateSerializer(serializers.ModelSerializer):
    """Create new payment ticket serializer"""

    class Meta:
        model = Ticket
        fields = [
            "client",
            "subject",
            "description",
            "priority",
            "source",
            "assigned_to",
            "related_invoice",
            "related_subscription",
            "payment_amount",
            "stripe_payment_intent_id",
        ]
        
    def validate(self, data):
        if not data.get('related_invoice') and not data.get('related_subscription'):
            raise serializers.ValidationError("Ticket must be linked to either an invoice or subscription.")
        return data


class TicketStatsSerializer(serializers.Serializer):
    """Ticket statistics serializer"""

    total_tickets = serializers.IntegerField()
    new_tickets = serializers.IntegerField()
    processing_payments = serializers.IntegerField()
    payment_failed = serializers.IntegerField()
    payment_disputed = serializers.IntegerField()
    refund_requested = serializers.IntegerField()
    resolved_tickets = serializers.IntegerField()
    total_payment_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_refund_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    avg_response_time = serializers.FloatField()
    avg_resolution_time = serializers.FloatField()
    tickets_by_priority = serializers.DictField()
    tickets_by_source = serializers.DictField()
