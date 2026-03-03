from rest_framework import serializers
from admin_portal.models import Report

class ReportSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    description = serializers.CharField()
    status = serializers.CharField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    

    formatted_date = serializers.SerializerMethodField()
    file_size = serializers.CharField(source='file_size_display', read_only=True) # "2.4 MB"
    download_url = serializers.FileField(source='file', read_only=True)
    
    def get_formatted_date(self, obj):
        return obj.created_at.strftime("%-m/%-d/%Y")