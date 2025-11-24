from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from ...models import ContactMessage
from ..serializers.contact import ContactMessageSerializer


class ContactRequestView(APIView):
    def post(self, request):
        serializer = ContactMessageSerializer(data=request.data)
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
       