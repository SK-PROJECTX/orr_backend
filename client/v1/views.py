import logging
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import status, views
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import SignUpSerializer, VerifyEmailSerializer, LoginSerializer, PasswordResetConfirmSerializer, PasswordResetRequestSerializer, ChangePasswordSerializer
from services.notifications.email_verification import send_email_verification_notification
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import (
    default_token_generator,
)
from rest_framework import generics, permissions


User = get_user_model()
from rest_framework.views import APIView


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
    
class VerifyEmailView(views.APIView):
    permission_classes = [AllowAny]
    serializer_class = VerifyEmailSerializer

    def post(self, request, *args, **kwargs):
        uid = request.data.get("uid")
        token = request.data.get("token")

        if not uid or not token:
            return Response(
                {"detail": "uid and token are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except Exception:
            return Response(
                {"detail": "Invalid UID."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not default_token_generator.check_token(user, token):
            return Response(
                {"detail": "Invalid or expired token."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.is_active = True
        user.save()

        return Response(
            {"message": "Email verified successfully. You may now log in."},
            status=status.HTTP_200_OK,
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

        # JWT generation
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
    
class PasswordResetRequestView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "No user found with this email."},
                status=status.HTTP_404_NOT_FOUND,
            )
        try:
            send_password_reset_notification(user)
        except Exception as e:
            return Response(
                {"error": f"Failed to send reset email: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {"message": "Password reset link sent."}, status=status.HTTP_200_OK
        )
class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, uidb64, token, *args, **kwargs):
        serializer = self.get_serializer(
            data={**request.data, "uid": uidb64, "token": token}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Password reset successful."}, status=status.HTTP_200_OK
        )

class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "message": "Password updated successfully",
            },
            status=status.HTTP_200_OK,
        )
