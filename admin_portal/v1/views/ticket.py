from django.db.models import Avg, Count, Q
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from admin_portal.models import Ticket, TicketMessage
from admin_portal.services import NotificationService
from ..serializers.ticket import (
    TicketCreateSerializer,
    TicketDetailSerializer,
    TicketListSerializer,
    TicketMessageSerializer,
    TicketStatsSerializer,
    TicketUpdateSerializer,
)


@extend_schema(
    tags=["Ticket Management"],
    summary="List or create tickets",
    description="Retrieve a filtered list of support tickets or create new tickets. Supports filtering by status, priority, assigned user, source, and date range.",
)
class TicketListView(generics.ListCreateAPIView):
    """List and create tickets"""

    permission_classes = [CanManageTickets]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return TicketCreateSerializer
        return TicketListSerializer

    def get_queryset(self):
        queryset = Ticket.objects.select_related("client__user", "assigned_to").all()

        # Search functionality
        search = self.request.query_params.get("search", None)
        if search:
            queryset = queryset.filter(
                Q(ticket_id__icontains=search)
                | Q(subject__icontains=search)
                | Q(client__user__first_name__icontains=search)
                | Q(client__user__last_name__icontains=search)
                | Q(client__company__icontains=search)
            )

        # Filters
        status_filter = self.request.query_params.get("status", None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        priority = self.request.query_params.get("priority", None)
        if priority:
            queryset = queryset.filter(priority=priority)

        assigned_to = self.request.query_params.get("assigned_to", None)
        if assigned_to:
            if assigned_to == "unassigned":
                queryset = queryset.filter(assigned_to__isnull=True)
            else:
                queryset = queryset.filter(assigned_to_id=assigned_to)

        source = self.request.query_params.get("source", None)
        if source:
            queryset = queryset.filter(source=source)

        # Date range filter
        date_from = self.request.query_params.get("date_from", None)
        date_to = self.request.query_params.get("date_to", None)
        if date_from:
            queryset = queryset.filter(created_at__gte=date_from)
        if date_to:
            queryset = queryset.filter(created_at__lte=date_to)

        return queryset.order_by("-created_at")

    def perform_create(self, serializer):
        # Generate ticket ID
        ticket = serializer.save()
        ticket.ticket_id = f"TKT-{timezone.now().strftime('%Y%m%d')}-{ticket.pk:03d}"
        ticket.save()


@extend_schema(
    tags=["Ticket Management"],
    summary="Get or update ticket details",
    description="Retrieve detailed information about a specific ticket or update ticket properties including status, priority, and assignments.",
)
class TicketDetailView(generics.RetrieveUpdateAPIView):
    """Get and update ticket details"""

    queryset = Ticket.objects.select_related("client__user", "assigned_to").all()
    permission_classes = [CanManageTickets]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return TicketDetailSerializer
        return TicketUpdateSerializer


@extend_schema(
    tags=["Ticket Management"],
    summary="Manage ticket messages",
    description="Retrieve all messages in a ticket conversation or add new messages. Messages can be marked as internal (admin-only) or public (visible to client).",
)
class TicketMessagesView(generics.ListCreateAPIView):
    """List and create ticket messages"""

    serializer_class = TicketMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        ticket_id = self.kwargs.get("ticket_id")
        return TicketMessage.objects.filter(ticket_id=ticket_id).order_by("created_at")

    def perform_create(self, serializer):
        ticket_id = self.kwargs.get("ticket_id")
        serializer.save(ticket_id=ticket_id, sender=self.request.user)


@extend_schema(
    tags=["Ticket Management"],
    summary="Perform ticket actions",
    description="Execute various ticket management actions including assign/unassign, update status/priority, and link to meetings or content.",
)
class TicketActionsView(APIView):
    """Ticket management actions"""

    permission_classes = [CanManageTickets]

    def post(self, request, pk):
        try:
            ticket = Ticket.objects.get(pk=pk)
            action = request.data.get("action")

            if action == "assign":
                assigned_to_id = request.data.get("assigned_to")
                if assigned_to_id:
                    from django.contrib.auth.models import User

                    try:
                        assigned_user = User.objects.get(pk=assigned_to_id)
                        ticket.assigned_to = assigned_user
                        ticket.save()
                        
                        # Send notification
                        NotificationService.send_ticket_notification(
                            ticket, 'assigned', assigned_user
                        )

                        return Response({"message": "Ticket assigned successfully"})
                    except User.DoesNotExist:
                        return Response(
                            {"error": "User not found"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                else:
                    # Unassign ticket
                    ticket.assigned_to = None
                    ticket.save()
                    return Response({"message": "Ticket unassigned"})

            elif action == "update_status":
                new_status = request.data.get("status")
                if new_status in dict(Ticket.STATUS_CHOICES):
                    ticket.status = new_status
                    ticket.save()
                    return Response(
                        {
                            "message": f"Ticket status updated to {new_status}",
                            "status": ticket.status,
                        }
                    )
                else:
                    return Response(
                        {"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST
                    )

            elif action == "update_priority":
                new_priority = request.data.get("priority")
                if new_priority in dict(Ticket.PRIORITY_CHOICES):
                    ticket.priority = new_priority
                    ticket.save()
                    return Response(
                        {
                            "message": f"Ticket priority updated to {new_priority}",
                            "priority": ticket.priority,
                        }
                    )
                else:
                    return Response(
                        {"error": "Invalid priority"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            elif action == "link_meeting":
                meeting_id = request.data.get("meeting_id")
                if meeting_id:
                    from admin_portal.models import Meeting

                    try:
                        meeting = Meeting.objects.get(pk=meeting_id)
                        ticket.related_meeting = meeting
                        ticket.save()
                        return Response({"message": "Meeting linked to ticket"})
                    except Meeting.DoesNotExist:
                        return Response(
                            {"error": "Meeting not found"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                else:
                    ticket.related_meeting = None
                    ticket.save()
                    return Response({"message": "Meeting unlinked from ticket"})

            elif action == "link_content":
                content_id = request.data.get("content_id")
                if content_id:
                    from admin_portal.models import Content

                    try:
                        content = Content.objects.get(pk=content_id)
                        ticket.related_content = content
                        ticket.save()
                        return Response({"message": "Content linked to ticket"})
                    except Content.DoesNotExist:
                        return Response(
                            {"error": "Content not found"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                else:
                    ticket.related_content = None
                    ticket.save()
                    return Response({"message": "Content unlinked from ticket"})

            else:
                return Response(
                    {"error": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST
                )

        except Ticket.DoesNotExist:
            return Response(
                {"error": "Ticket not found"}, status=status.HTTP_404_NOT_FOUND
            )


@extend_schema(
    tags=["Ticket Management"],
    summary="Get ticket statistics",
    description="Retrieve comprehensive ticket analytics including counts by status/priority/source, average response times, and resolution metrics.",
)
class TicketStatsView(APIView):
    """Ticket statistics and analytics"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Basic ticket counts
        total_tickets = Ticket.objects.count()
        new_tickets = Ticket.objects.filter(status="new").count()
        in_progress_tickets = Ticket.objects.filter(status="in_progress").count()
        waiting_client_tickets = Ticket.objects.filter(status="waiting_client").count()
        resolved_tickets = Ticket.objects.filter(status="resolved").count()

        # Average response and resolution times (placeholder - would need actual calculation)
        avg_response_time = 2.5  # hours
        avg_resolution_time = 24.0  # hours

        # Tickets by priority
        tickets_by_priority = dict(
            Ticket.objects.values("priority")
            .annotate(count=Count("id"))
            .values_list("priority", "count")
        )

        # Tickets by source
        tickets_by_source = dict(
            Ticket.objects.values("source")
            .annotate(count=Count("id"))
            .values_list("source", "count")
        )

        stats_data = {
            "total_tickets": total_tickets,
            "new_tickets": new_tickets,
            "in_progress_tickets": in_progress_tickets,
            "waiting_client_tickets": waiting_client_tickets,
            "resolved_tickets": resolved_tickets,
            "avg_response_time": avg_response_time,
            "avg_resolution_time": avg_resolution_time,
            "tickets_by_priority": tickets_by_priority,
            "tickets_by_source": tickets_by_source,
        }

        serializer = TicketStatsSerializer(stats_data)
        return Response(serializer.data)


@extend_schema(
    tags=["Ticket Management"],
    summary="Get my assigned tickets",
    description="Retrieve all tickets assigned to the current authenticated user, ordered by creation date.",
)
class MyTicketsView(generics.ListAPIView):
    """Get tickets assigned to current user"""

    serializer_class = TicketListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Ticket.objects.filter(assigned_to=self.request.user)
            .select_related("client__user")
            .order_by("-created_at")
        )
