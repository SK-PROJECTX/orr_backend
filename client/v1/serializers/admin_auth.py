from django.contrib.auth import get_user_model
from rest_framework import serializers
from admin_portal.models import AdminRole

User = get_user_model()


class AdminSignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    admin_role = serializers.ChoiceField(choices=[], required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        role_choices = [(role.name, role.get_name_display()) for role in AdminRole.objects.all()]
        self.fields['admin_role'].choices = role_choices

    class Meta:
        model = User
        fields = ("username", "email", "password", "first_name", "last_name", "admin_role")