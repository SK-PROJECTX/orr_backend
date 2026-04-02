"""
Client-side ticket views for viewing tickets and auto-replies
"""

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from admin_portal.models import Ticket, TicketMessage
from admin_portal.v1.serializers.ticket import TicketDetailSerializer, TicketMessageSerializer


@extend_schema(
    tags=["Client Tickets"],
    summary="Get client's tickets",
    description="Retrieve all tickets for the authenticated client user.",
)
class ClientTicketListView(generics.ListAPIView):
    """List tickets for authenticated client"""
    
    permission_classes = [IsAuthenticated]
    serializer_class = TicketDetailSerializer

    def get_queryset(self):
        # Get tickets for the current user's client profile
        try:
            from admin_portal.models import Client
            from django.db.models import Max, Count, Q
            from django.db.models.functions import Coalesce
            
            client = Client.objects.get(user=self.request.user)
            return Ticket.objects.filter(client=client).annotate(
                last_message_at=Coalesce(Max('messages__created_at'), 'created_at'),
                messages_count=Count('messages', filter=Q(messages__is_internal=False))
            ).order_by('-last_message_at')
        except Client.DoesNotExist:
            return Ticket.objects.none()


@extend_schema(
    tags=["Client Tickets"],
    summary="Get ticket details with messages",
    description="Retrieve detailed ticket information including all messages for the authenticated client.",
)
class ClientTicketDetailView(generics.RetrieveAPIView):
    """Get ticket details with messages for client"""
    
    permission_classes = [IsAuthenticated]
    serializer_class = TicketDetailSerializer

    def get_queryset(self):
        try:
            from admin_portal.models import Client
            client = Client.objects.get(user=self.request.user)
            return Ticket.objects.filter(client=client)
        except Client.DoesNotExist:
            return Ticket.objects.none()


@extend_schema(
    tags=["Client Tickets"],
    summary="Get ticket messages",
    description="Retrieve all messages for a specific ticket (client-visible only).",
)
class ClientTicketMessagesView(generics.ListAPIView):
    """Get messages for a specific ticket (client-visible only)"""
    
    permission_classes = [IsAuthenticated]
    serializer_class = TicketMessageSerializer

    def get_queryset(self):
        ticket_id = self.kwargs.get('ticket_id')
        
        # Verify the ticket belongs to the current user
        try:
            from admin_portal.models import Client
            client = Client.objects.get(user=self.request.user)
            ticket = Ticket.objects.get(id=ticket_id, client=client)
            
            # Return only non-internal messages (visible to client)
            return TicketMessage.objects.filter(
                ticket=ticket, 
                is_internal=False
            ).order_by('created_at')
        except (Client.DoesNotExist, Ticket.DoesNotExist):
            return TicketMessage.objects.none()


@extend_schema(
    tags=["Client Tickets"],
    summary="Send message to ticket",
    description="Send a new message to an existing ticket.",
)
class ClientSendMessageView(APIView):
    """Send a message to a ticket"""
    
    permission_classes = [IsAuthenticated]

    def post(self, request, ticket_id):
        try:
            from admin_portal.models import Client
            client = Client.objects.get(user=self.request.user)
            ticket = Ticket.objects.get(id=ticket_id, client=client)
            
            message_text = request.data.get('message', '').strip()
            if not message_text:
                return Response(
                    {"error": "Message cannot be empty"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Create the message
            message = TicketMessage.objects.create(
                ticket=ticket,
                sender=request.user,
                message=message_text,
                is_internal=False  # Client messages are always visible
            )
            
            # Update ticket status if it was resolved
            if ticket.status == 'resolved':
                ticket.status = 'new'
                ticket.save()
            
            serializer = TicketMessageSerializer(message)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except Client.DoesNotExist:
            return Response(
                {"error": "Client profile not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Ticket.DoesNotExist:
            return Response(
                {"error": "Ticket not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )