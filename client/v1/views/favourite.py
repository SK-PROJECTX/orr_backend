from ...models import FavoriteDocument
from ..serializers.favourite import  FavoriteDocumentSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from admin_portal.models import ClientDocument
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from django.shortcuts import get_object_or_404

@extend_schema(tags=["favoutite"])
class FavoriteListView(generics.ListAPIView):
    serializer_class = FavoriteDocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FavoriteDocument.objects.filter(user=self.request.user)

@extend_schema(tags=["favoutite"])
class ToggleFavoriteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, document_id):
        user = request.user
        document = get_object_or_404(ClientDocument, id=document_id)

        fav, created = FavoriteDocument.objects.get_or_create(
            user=user,
            document=document
        )

        if not created:
            fav.delete()
            return Response({
                "success": True,
                "message": "Removed from favorites"
            })

        return Response({
            "success": True,
            "message": "Added to favorites"
        })
    
@extend_schema(tags=["favoutite"])
class FavoriteDeleteView(generics.DestroyAPIView):
    serializer_class = FavoriteDocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FavoriteDocument.objects.filter(user=self.request.user)

