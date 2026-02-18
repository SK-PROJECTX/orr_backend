from rest_framework import serializers
from admin_portal.models import Meeting

class PastConsultationSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.user.get_full_name', read_only=True)
    
    type_display = serializers.CharField(source='get_meeting_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    formatted_date = serializers.SerializerMethodField()
    formatted_time = serializers.SerializerMethodField()
    
    # Missing Model Fields (Handled for UI compatibility)
    # The image shows a 'Rating' and 'Outcome', which aren't in your model yet.
    # We will map 'Outcome' to 'internal_notes' for now, or return a default.
    outcome = serializers.CharField(source='internal_notes', read_only=True) 
    rating = serializers.SerializerMethodField() 

    class Meta:
        model = Meeting
        fields = [
            'id',
            'title',            
            'type_display',    
            'status',          
            'status_display',   
            'color',            
            'formatted_date',  
            'formatted_time',   
            'meeting_notes',  
            'outcome',         
            'rating',           # Placeholder for the star rating
            'meeting_link',     # For "View Details" or joining
        ]

    def get_formatted_date(self, obj):
        """Matches UI format: Sun, Jan 14, 2024"""
        dt = obj.confirmed_datetime or obj.requested_datetime
        if dt:
            return dt.strftime("%a, %b %d, %Y")
        return "TBD"

    def get_formatted_time(self, obj):
        """Matches UI format: 60 min"""
        return f"{obj.duration_minutes} min"

    def get_rating(self, obj):
        #Todo: Add rating = models.IntegerField() to the Meeting model.
        return 5