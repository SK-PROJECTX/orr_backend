from django.db.models import Q
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from admin_portal.models import Client, Content, Meeting, Ticket
from common.permissions import IsAdminUser

from ..serializers.client import ClientListSerializer
from ..serializers.content import ContentListSerializer
from ..serializers.meeting import MeetingListSerializer
from ..serializers.ticket import TicketListSerializer


@extend_schema(
    tags=["Search & Navigation"],
    summary="Global search across all admin portal data",
    description="Search across clients, tickets, content, and meetings with a single query string.",
    parameters=[
        OpenApiParameter(
            name="q",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="Search query string",
            required=True,
        ),
        OpenApiParameter(
            name="type",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="Filter by content type: clients, tickets, meetings, content, or all",
            enum=["clients", "tickets", "meetings", "content", "all"],
        ),
        OpenApiParameter(
            name="limit",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description="Maximum results per category (default: 10)",
        ),
    ],
)
class GlobalSearchView(APIView):
    """Global search across all admin portal entities"""

    permission_classes = [IsAdminUser]

    def get(self, request):
        query = request.query_params.get("q", "").strip()
        search_type = request.query_params.get("type", "all")
        limit = int(request.query_params.get("limit", 10))

        if not query:
            return Response(
                {
                    "query": query,
                    "results": {
                        "clients": [],
                        "tickets": [],
                        "meetings": [],
                        "content": [],
                    },
                    "total_count": 0,
                }
            )

        results = {}
        total_count = 0

        # Search clients
        if search_type in ["clients", "all"]:
            clients = self._search_clients(query, limit)
            results["clients"] = ClientListSerializer(clients, many=True).data
            total_count += len(clients)

        # Search tickets
        if search_type in ["tickets", "all"]:
            tickets = self._search_tickets(query, limit)
            results["tickets"] = TicketListSerializer(tickets, many=True).data
            total_count += len(tickets)

        # Search meetings
        if search_type in ["meetings", "all"]:
            meetings = self._search_meetings(query, limit)
            results["meetings"] = MeetingListSerializer(meetings, many=True).data
            total_count += len(meetings)

        # Search content
        if search_type in ["content", "all"]:
            content = self._search_content(query, limit)
            results["content"] = ContentListSerializer(content, many=True).data
            total_count += len(content)

        return Response(
            {"query": query, "results": results, "total_count": total_count}
        )

    def _search_clients(self, query, limit):
        """Search clients by name, company, email"""
        return Client.objects.select_related("user").filter(
            Q(user__first_name__icontains=query)
            | Q(user__last_name__icontains=query)
            | Q(user__email__icontains=query)
            | Q(company__icontains=query)
        )[:limit]

    def _search_tickets(self, query, limit):
        """Search tickets by ID, subject, description"""
        return Ticket.objects.select_related("client__user").filter(
            Q(ticket_id__icontains=query)
            | Q(subject__icontains=query)
            | Q(description__icontains=query)
        )[:limit]

    def _search_meetings(self, query, limit):
        """Search meetings by client name, agenda"""
        return Meeting.objects.select_related("client__user").filter(
            Q(client__user__first_name__icontains=query)
            | Q(client__user__last_name__icontains=query)
            | Q(client__company__icontains=query)
            | Q(agenda__icontains=query)
        )[:limit]

    def _search_content(self, query, limit):
        """Search content by title, summary, content"""
        return Content.objects.filter(
            Q(title__icontains=query)
            | Q(summary__icontains=query)
            | Q(content__icontains=query)
        )[:limit]


@extend_schema(
    tags=["Search & Navigation"],
    summary="Quick search suggestions",
    description="Get quick search suggestions as user types for autocomplete functionality.",
    parameters=[
        OpenApiParameter(
            name="q",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="Partial search query",
            required=True,
        )
    ],
)
class QuickSearchView(APIView):
    """Quick search suggestions for autocomplete"""

    permission_classes = [IsAdminUser]

    def get(self, request):
        query = request.query_params.get("q", "").strip()

        if len(query) < 2:
            return Response({"suggestions": []})

        suggestions = []

        # Client suggestions
        clients = Client.objects.select_related("user").filter(
            Q(user__first_name__icontains=query)
            | Q(user__last_name__icontains=query)
            | Q(company__icontains=query)
        )[:5]

        for client in clients:
            suggestions.append(
                {
                    "type": "client",
                    "id": client.id,
                    "title": f"{client.user.get_full_name()} - {client.company}",
                    "url": f"/admin/clients/{client.id}/",
                }
            )

        # Ticket suggestions
        tickets = Ticket.objects.filter(
            Q(ticket_id__icontains=query) | Q(subject__icontains=query)
        )[:5]

        for ticket in tickets:
            suggestions.append(
                {
                    "type": "ticket",
                    "id": ticket.id,
                    "title": f"{ticket.ticket_id} - {ticket.subject}",
                    "url": f"/admin/tickets/{ticket.id}/",
                }
            )

        # Content suggestions
        content = Content.objects.filter(Q(title__icontains=query), status="published")[
            :5
        ]

        for item in content:
            suggestions.append(
                {
                    "type": "content",
                    "id": item.id,
                    "title": item.title,
                    "url": f"/admin/content/{item.id}/",
                }
            )

        return Response(
            {"suggestions": suggestions[:15]}
        )  # Limit to 15 total suggestions
