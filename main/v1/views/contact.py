from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.contact import ContactMessageSerializer
from drf_spectacular.utils import extend_schema


@extend_schema(tags=["main page"])
class ContactMessageView(APIView):
    serializer_class = ContactMessageSerializer

    def post(self, request):
        serializer = ContactMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Message sent successfully"}, status=200)
        return Response(serializer.errors, status=400)
