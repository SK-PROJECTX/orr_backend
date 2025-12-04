import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from drf_spectacular.utils import extend_schema
from rest_framework import status, views
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


from services.notifications.email_verification import (
    send_email_verification_notification,
)

from ..serializers.client_auth import ClientSignUpSerializer

User = get_user_model()


@extend_schema(tags=["Client Authentication"])
class ClientSignupView(views.APIView):
    permission_classes = [AllowAny]
    serializer_class = ClientSignUpSerializer

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
            is_active=False,
        )
        user.set_password(password)
        user.save()
        try:
            send_email_verification_notification(user)
        except Exception as e:
            logging.error(f"Client signup email failed to send: {e}")

        return Response(
            {"detail": "Client registration successful. Email sent."},
            status=status.HTTP_201_CREATED,
        )
