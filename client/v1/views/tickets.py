from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from admin_portal.models import Ticket, Client
from ..serializers.tickets import TicketHistorySerializer , ClientInquiryTicketSerializer
from rest_framework import status
from drf_spectacular.utils import extend_schema


@extend_schema(
    tags=["Ticket"],
)
class ClientTicketHistoryAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TicketHistorySerializer
    def get(self, request):
        user = request.user
        client = Client.objects.get(user=user)

        if not client:
            return Response(
                {"detail": "Client profile not found"},
                status=400,
            )

        tickets = (
            Ticket.objects
            .filter(client=client)
            .order_by("-created_at")
        )

        serializer = TicketHistorySerializer(tickets, many=True)
        return Response(serializer.data)



@extend_schema(
    tags=["Ticket"],
)
class ClientTicketCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClientInquiryTicketSerializer
    def post(self, request):
        user = request.user
        client = Client.objects.get(user=user)

        if not client:
            return Response(
                {"detail": "Client profile not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = ClientInquiryTicketSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ticket = serializer.save(
            client=client,

        )

        return Response(
            {
                "message": "Ticket created successfully",
                "ticket_id": ticket.ticket_id,
            },
            status=status.HTTP_201_CREATED,
        )