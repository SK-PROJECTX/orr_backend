from rest_framework import serializers
from admin_portal.models import AIConversation


class AIConversationListSerializer(serializers.ModelSerializer):
    """AI conversation list serializer"""
    client_name = serializers.CharField(source='client.user.get_full_name')
    client_email = serializers.CharField(source='client.user.email')
    reviewed_by_name = serializers.CharField(source='reviewed_by.get_full_name', allow_null=True)
    
    class Meta:
        model = AIConversation
        fields = [
            'id', 'session_id', 'client_name', 'client_email', 'summary',
            'escalated_to_ticket', 'needs_improvement', 'reviewed_by_name',
            'created_at'
        ]


class AIConversationDetailSerializer(serializers.ModelSerializer):
    """Detailed AI conversation serializer"""
    client_name = serializers.CharField(source='client.user.get_full_name')
    client_email = serializers.CharField(source='client.user.email')
    client_company = serializers.CharField(source='client.company')
    reviewed_by_name = serializers.CharField(source='reviewed_by.get_full_name', allow_null=True)
    message_count = serializers.SerializerMethodField()
    
    class Meta:
        model = AIConversation
        fields = [
            'id', 'session_id', 'client_name', 'client_email', 'client_company',
            'messages', 'summary', 'escalated_to_ticket', 'escalation_reason',
            'needs_improvement', 'improvement_notes', 'reviewed_by_name',
            'message_count', 'created_at', 'updated_at'
        ]
    
    def get_message_count(self, obj):
        return len(obj.messages) if obj.messages else 0


class AIConversationStatsSerializer(serializers.Serializer):
    """AI conversation statistics serializer"""
    total_conversations = serializers.IntegerField()
    conversations_7d = serializers.IntegerField()
    conversations_30d = serializers.IntegerField()
    escalation_rate_overall = serializers.FloatField()
    escalation_rate_7d = serializers.FloatField()
    needs_improvement = serializers.IntegerField()
    reviewed_conversations = serializers.IntegerField()
    daily_conversations = serializers.ListField()