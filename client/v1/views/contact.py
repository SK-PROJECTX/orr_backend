from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from ...models import ContactMessage
from ..serializers.contact import SupportMessageSerializer, CreateSupportMessageSerializer
from rest_framework import generics, permissions

class ContactRequestView(APIView):
    serializer_class = CreateSupportMessageSerializer
    def post(self, request):
        serializer = CreateSupportMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        
        contact = ContactMessage.objects.create(
            name=data["name"],
            email=data["email"],
            website=data.get("website", ""),
            message=data["message"],
        )

        return Response(
            {"message": "Your message has been sent successfully."},
            status=status.HTTP_201_CREATED,
        )

class SupportHistoryListView(generics.ListAPIView):
    serializer_class = SupportMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ContactMessage.objects.all().order_by("-created_at")
    
class SupportMessageUpdateView(generics.UpdateAPIView):
    serializer_class = SupportMessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = "message_id"

    def get_queryset(self):
        return ContactMessage.objects.all()

    def patch(self, request, *args, **kwargs):
        message = self.get_object()

        is_read = request.data.get("is_read")
        if is_read is None:
            return Response(
                {"error": "is_read field is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        message.is_read = bool(is_read)
        message.save()

        return Response(
            {"message": "Support message updated", "is_read": message.is_read},
            status=status.HTTP_200_OK
        )
