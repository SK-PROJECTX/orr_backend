from rest_framework import serializers

from ..models import Invoice, PricingPlan


class CreateCheckoutSerializer(serializers.Serializer):
    price_id = serializers.CharField()


class ChangePlanSerializer(serializers.Serializer):
    price_id = serializers.CharField()
    prorate = serializers.BooleanField(default=True)


class PauseSubscriptionSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=["pause", "resume"])
    behavior = serializers.ChoiceField(
        choices=["keep_as_draft", "mark_uncollectible", "void"], required=False
    )
    resumes_at = serializers.DateTimeField(required=False)


class BillingPortalSerializer(serializers.Serializer):
    return_url = serializers.URLField()


class InvoiceHistorySerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='user.get_full_name', read_only=True)
    client_email = serializers.CharField(source='user.email', read_only=True)
    reference_id = serializers.CharField(source='stripe_invoice_id', read_only=True)
    transaction_date = serializers.CharField(source='billing_date', read_only=True)
    payment_method = serializers.SerializerMethodField()
    
    def get_payment_method(self, obj):
        return "Credit Card"
    
    class Meta:
        model = Invoice
        fields = [
            "id",
            "reference_id",
            "transaction_date",
            "client_name",
            "client_email",
            "payment_method",
            "amount",
            "status",
            "billing_title",
            "currency",
            "plan",
            "users",
            "invoice_pdf",
            "hosted_invoice_url",
        ]


class PricingPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricingPlan
        fields = "__all__"
        read_only_fields = ("stripe_price_id",)
