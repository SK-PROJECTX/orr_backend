from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from admin_portal.models import Meeting
from ..serializers.past_consultation import PastConsultationSerializer


from drf_spectacular.utils import extend_schema

@extend_schema(tags=["past consultation"])
class PastConsultationListView(generics.ListAPIView):
    serializer_class = PastConsultationSerializer
    filter_backends = [
        DjangoFilterBackend, 
        filters.SearchFilter, 
        filters.OrderingFilter
    ]
    
    queryset = Meeting.objects.filter(
        status__in=['completed', 'cancelled', 'declined', 'confirmed']
    )

   
    filterset_fields = ['status', 'meeting_type']

    search_fields = ['client__user__first_name', 'client__user__last_name', 'meeting_type']

  
    ordering_fields = ['confirmed_datetime', 'requested_datetime']
    ordering = ['-confirmed_datetime'] 