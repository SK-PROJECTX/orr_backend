import logging
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import status, views
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from services.notifications.email_verification import send_email_verification_notification
from admin_portal.models import AdminRole, AdminProfile
from ..serializers.admin_auth import AdminSignUpSerializer

User = get_user_model()


@extend_schema(tags=["Admin Authentication"])
@method_decorator(csrf_exempt, name='dispatch')
class AdminSignupView(views.APIView):
    permission_classes = [AllowAny]
    serializer_class = AdminSignUpSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(
                {"error": "Invalid data.", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        username = serializer.validated_data["username"]
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        first_name = serializer.validated_data["first_name"]
        last_name = serializer.validated_data["last_name"]
        admin_role = serializer.validated_data["admin_role"]

        try:
            validate_password(password)
        except Exception as exc:
            return Response(
                {"error": "Weak password.", "details": exc.messages},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {"message": "Username already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if User.objects.filter(email=email).exists():
            return Response(
                {"message": "Email already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User(
            username=username, 
            email=email, 
            first_name=first_name,
            last_name=last_name,
            is_active=False
        )
        user.set_password(password)
        user.save()

        # Create admin profile
        role_instance = AdminRole.objects.get(name=admin_role)
        AdminProfile.objects.create(
            user=user,
            role=role_instance
        )

        try:
            send_email_verification_notification(user)
        except Exception as e:
            logging.error(f"Admin signup email failed to send: {e}")

        return Response(
            {"detail": "Admin registration successful. Email sent."},
            status=status.HTTP_201_CREATED,
        )