from rest_framework.permissions import  IsAuthenticated
from ..serializers.document import ClientDocumentSerializer
from rest_framework import generics
from admin_portal.models import ClientDocument
from drf_spectacular.utils import extend_schema

@extend_schema(tags=["document"])
class ClientDocumentsView(generics.ListAPIView):
    serializer_class = ClientDocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        client = getattr(user, "client_profile", None)
        if not client:
            return ClientDocument.objects.none()

        return client.documents.filter(is_visible_to_client=True)
