from django.db.models import Count, Q
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from admin_portal.models import AIConversation

from ..serializers.ai_oversight import (
    AIConversationDetailSerializer,
    AIConversationListSerializer,
    AIConversationStatsSerializer,
)


@extend_schema(
    tags=["AI & Chat Oversight"],
    summary="List AI conversations",
    description="Retrieve a filtered list of AI chat conversations with options to filter by client, escalation status, and improvement flags.",
)
class AIConversationListView(generics.ListAPIView):
    """List AI chat conversations"""

    serializer_class = AIConversationListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = AIConversation.objects.select_related("client__user").all()

        # Search functionality
        search = self.request.query_params.get("search", None)
        if search:
            queryset = queryset.filter(
                Q(client__user__first_name__icontains=search)
                | Q(client__user__last_name__icontains=search)
                | Q(client__user__email__icontains=search)
                | Q(session_id__icontains=search)
                | Q(summary__icontains=search)
            )

        # Filters
        escalated = self.request.query_params.get("escalated", None)
        if escalated is not None:
            queryset = queryset.filter(escalated_to_ticket=escalated.lower() == "true")

        needs_improvement = self.request.query_params.get("needs_improvement", None)
        if needs_improvement is not None:
            queryset = queryset.filter(
                needs_improvement=needs_improvement.lower() == "true"
            )

        client_id = self.request.query_params.get("client", None)
        if client_id:
            queryset = queryset.filter(client_id=client_id)

        # Date range filter
        date_from = self.request.query_params.get("date_from", None)
        date_to = self.request.query_params.get("date_to", None)
        if date_from:
            queryset = queryset.filter(created_at__gte=date_from)
        if date_to:
            queryset = queryset.filter(created_at__lte=date_to)

        return queryset.order_by("-created_at")


@extend_schema(
    tags=["AI & Chat Oversight"],
    summary="Get AI conversation details",
    description="Retrieve detailed information about a specific AI conversation including full message history and any improvement notes.",
)
class AIConversationDetailView(generics.RetrieveAPIView):
    """Get AI conversation details"""

    queryset = AIConversation.objects.select_related(
        "client__user", "reviewed_by"
    ).all()
    serializer_class = AIConversationDetailSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(
    tags=["AI & Chat Oversight"],
    summary="Perform AI conversation actions",
    description="Execute actions on AI conversations including mark for improvement, add review notes, or mark as reviewed.",
)
class AIConversationActionsView(APIView):
    """AI conversation management actions"""

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            conversation = AIConversation.objects.get(pk=pk)
            action = request.data.get("action")

            if action == "mark_needs_improvement":
                conversation.needs_improvement = True
                notes = request.data.get("notes", "")
                if notes:
                    conversation.improvement_notes = notes
                conversation.save()
                return Response({"message": "Conversation marked for improvement"})

            elif action == "mark_reviewed":
                conversation.needs_improvement = False
                conversation.reviewed_by = request.user
                notes = request.data.get("notes", "")
                if notes:
                    conversation.improvement_notes = notes
                conversation.save()
                return Response({"message": "Conversation marked as reviewed"})

            elif action == "add_notes":
                notes = request.data.get("notes", "")
                if notes:
                    conversation.improvement_notes = notes
                    conversation.save()
                    return Response({"message": "Notes added successfully"})
                else:
                    return Response(
                        {"error": "Notes are required"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            else:
                return Response(
                    {"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST
                )

        except AIConversation.DoesNotExist:
            return Response(
                {"error": "Conversation not found"}, status=status.HTTP_404_NOT_FOUND
            )


@extend_schema(
    tags=["AI & Chat Oversight"],
    summary="Get AI conversation statistics",
    description="Retrieve comprehensive AI chat statistics including total conversations, escalation rates, improvement flags, and trends over time.",
)
class AIConversationStatsView(APIView):
    """AI conversation statistics"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        from datetime import timedelta

        from django.utils import timezone

        now = timezone.now()
        last_7_days = now - timedelta(days=7)
        last_30_days = now - timedelta(days=30)

        # Basic counts
        total_conversations = AIConversation.objects.count()
        conversations_7d = AIConversation.objects.filter(
            created_at__gte=last_7_days
        ).count()
        conversations_30d = AIConversation.objects.filter(
            created_at__gte=last_30_days
        ).count()

        # Escalation metrics
        total_escalated = AIConversation.objects.filter(
            escalated_to_ticket=True
        ).count()
        escalated_7d = AIConversation.objects.filter(
            escalated_to_ticket=True, created_at__gte=last_7_days
        ).count()

        # Calculate escalation rates
        escalation_rate_overall = (
            (total_escalated / total_conversations * 100)
            if total_conversations > 0
            else 0
        )
        escalation_rate_7d = (
            (escalated_7d / conversations_7d * 100) if conversations_7d > 0 else 0
        )

        # Improvement metrics
        needs_improvement = AIConversation.objects.filter(
            needs_improvement=True
        ).count()
        reviewed_conversations = AIConversation.objects.filter(
            reviewed_by__isnull=False
        ).count()

        # Daily conversation counts for last 7 days
        daily_conversations = []
        for i in range(7):
            date = (now - timedelta(days=i)).date()
            count = AIConversation.objects.filter(created_at__date=date).count()
            escalated_count = AIConversation.objects.filter(
                created_at__date=date, escalated_to_ticket=True
            ).count()
            daily_conversations.append(
                {
                    "date": date.isoformat(),
                    "conversations": count,
                    "escalated": escalated_count,
                }
            )

        stats_data = {
            "total_conversations": total_conversations,
            "conversations_7d": conversations_7d,
            "conversations_30d": conversations_30d,
            "escalation_rate_overall": round(escalation_rate_overall, 2),
            "escalation_rate_7d": round(escalation_rate_7d, 2),
            "needs_improvement": needs_improvement,
            "reviewed_conversations": reviewed_conversations,
            "daily_conversations": daily_conversations,
        }

        serializer = AIConversationStatsSerializer(stats_data)
        return Response(serializer.data)
