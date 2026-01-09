"""
Auto Reply API Views
Provides endpoints for managing automatic replies to client tickets
"""

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter

from admin_portal.models import Ticket
from admin_portal.permissions import CanManageTickets
from admin_portal.auto_reply_service import AutoReplyService


@extend_schema(
    tags=["Auto Reply Management"],
    summary="Send automatic reply to ticket",
    description="Send various types of automatic replies to client tickets with customizable timeframes.",
)
class AutoReplyView(APIView):
    """Manage automatic replies for tickets"""
    
    permission_classes = [CanManageTickets]

    def post(self, request, ticket_id):
        """Send automatic reply to a specific ticket"""
        try:
            ticket = Ticket.objects.get(pk=ticket_id)
        except Ticket.DoesNotExist:
            return Response(
                {"error": "Ticket not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

        reply_type = request.data.get("reply_type", "initial")
        custom_timeframe = request.data.get("timeframe", "24 hours")

        success = False
        message = ""

        if reply_type == "initial":
            success = AutoReplyService.send_initial_auto_reply(ticket, custom_timeframe)
            message = "Initial auto-reply sent successfully"
            
        elif reply_type == "delay_notice":
            success = AutoReplyService.send_delay_notice(ticket, custom_timeframe)
            message = "Delay notice sent successfully"
            
        elif reply_type == "review_message":
            success = AutoReplyService.send_review_message(ticket, custom_timeframe)
            message = "Review message sent successfully"
            
        else:
            return Response(
                {"error": "Invalid reply_type. Use: initial, delay_notice, or review_message"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if success:
            return Response({
                "message": message,
                "ticket_id": ticket.ticket_id,
                "reply_type": reply_type,
                "timeframe": custom_timeframe
            })
        else:
            return Response(
                {"error": "Failed to send auto-reply"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema(
    tags=["Auto Reply Management"],
    summary="Schedule delayed auto-reply",
    description="Schedule an automatic reply to be sent after a specified delay.",
)
class ScheduleAutoReplyView(APIView):
    """Schedule automatic replies for later delivery"""
    
    permission_classes = [CanManageTickets]

    def post(self, request, ticket_id):
        """Schedule a delayed auto-reply"""
        try:
            ticket = Ticket.objects.get(pk=ticket_id)
        except Ticket.DoesNotExist:
            return Response(
                {"error": "Ticket not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

        delay_minutes = request.data.get("delay_minutes", 60)
        custom_timeframe = request.data.get("timeframe", "48 hours")

        try:
            delay_minutes = int(delay_minutes)
            if delay_minutes < 1:
                raise ValueError("Delay must be at least 1 minute")
        except (ValueError, TypeError):
            return Response(
                {"error": "Invalid delay_minutes. Must be a positive integer"},
                status=status.HTTP_400_BAD_REQUEST
            )

        success = AutoReplyService.schedule_delay_notice(
            ticket, delay_minutes, custom_timeframe
        )

        if success:
            return Response({
                "message": "Auto-reply scheduled successfully",
                "ticket_id": ticket.ticket_id,
                "delay_minutes": delay_minutes,
                "timeframe": custom_timeframe
            })
        else:
            return Response(
                {"error": "Failed to schedule auto-reply"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema(
    tags=["Auto Reply Management"],
    summary="Get auto-reply templates",
    description="Retrieve available auto-reply templates and their default content.",
)
class AutoReplyTemplatesView(APIView):
    """Get available auto-reply templates"""
    
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get all available auto-reply templates"""
        templates = {
            "initial_reply": {
                "name": "Initial Acknowledgment",
                "template": AutoReplyService.DEFAULT_INITIAL_REPLY,
                "description": "Sent immediately when a ticket is created"
            },
            "delay_notice": {
                "name": "Delay Notice",
                "template": AutoReplyService.DEFAULT_DELAY_NOTICE,
                "description": "Sent when additional time is needed for response",
                "supports_timeframe": True
            },
            "review_message": {
                "name": "Review Message", 
                "template": AutoReplyService.DEFAULT_REVIEW_MESSAGE,
                "description": "Sent when ticket is under detailed review",
                "supports_timeframe": True
            }
        }

        return Response({
            "templates": templates,
            "default_timeframes": [
                "24 hours",
                "48 hours", 
                "72 hours",
                "1 week",
                "2 weeks"
            ]
        })