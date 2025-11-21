from django.contrib.auth.password_validation import validate_password
from rest_framework.permissions import AllowAny
from rest_framework import status, views
from rest_framework.response import Response
from services.notifications.email_verification import send_email_verification_notification
from ..serializers.auth import SignUpSerializer, LoginSerializer
import logging
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
User = get_user_model()

class SignupView(views.APIView):
    permission_classes = [AllowAny]
    serializer_class = SignUpSerializer

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

        user = User(username=username, email=email, is_active=False)
        user.set_password(password)
        user.save()

        try:
            send_email_verification_notification(user)
        except Exception as e:
            logging.error(f"Signup email failed to send: {e}")

        return Response(
            {"detail": "Registration successful. Email sent."},
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, 
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

      
        if not user.is_active:
            send_email_verification_notification(user)
            return Response(
                {
                    "message": "Account not verified. A new verification email has been sent.",
                    "data": {},
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "status": status.HTTP_200_OK,
                "message": "Login successful",
                "data": {
                    "accessToken": str(refresh.access_token),
                    "refreshToken": str(refresh),
                },
            },
            status=status.HTTP_200_OK,
        )
    