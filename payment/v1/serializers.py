from rest_framework import serializers
from ..models import Invoice


class CreateCheckoutSerializer(serializers.Serializer):
    price_id = serializers.CharField()
    success_url = serializers.URLField()
    cancel_url = serializers.URLField()




class ChangePlanSerializer(serializers.Serializer):
    price_id = serializers.CharField()  
    prorate = serializers.BooleanField(default=True)  

class PauseSubscriptionSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=["pause", "resume"])
    behavior = serializers.ChoiceField(
        choices=["keep_as_draft", "mark_uncollectible", "void"],
        required=False
    )
    resumes_at = serializers.DateTimeField(required=False)

class BillingPortalSerializer(serializers.Serializer):
    return_url = serializers.URLField()

class InvoiceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = [
            "id",
            "billing_title",
            "status",
            "billing_date",
            "amount",
            "currency",
            "plan",
            "users",
            "invoice_pdf",
            "hosted_invoice_url"
        ]