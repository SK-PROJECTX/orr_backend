from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import generics, permissions, status, views
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from tasks.activities import rebuild_recommendations_cache
from services.activities.recommendation import get_recommended_steps
from django.core.cache import cache


from ..serializers.account import (
    AccountSettingsDetailsSerializer,
    ChangePasswordSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    VerifyEmailSerializer, ActivitySerializer
)

from client.models import Activity
from drf_spectacular.utils import extend_schema
from services.notifications.password_reset import send_password_reset_notification
User = get_user_model()

@extend_schema(tags=["account"])
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

@extend_schema(tags=["account"])
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

@extend_schema(tags=["account"])
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

@extend_schema(tags=["account-setting"])
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
        user = request.user
        user.set_password(serializer.validated_data["new_password"])
        user.save()
        return Response(
            {
                "message": "Password updated successfully",
            },
            status=status.HTTP_200_OK,
        )

@extend_schema(tags=["account-setting"])
class AccountSettingsView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AccountSettingsDetailsSerializer

    def patch(self, request):
        serializer = AccountSettingsDetailsSerializer(
            data=request.data,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        user = request.user
        profile = request.user.profile

        data = serializer.validated_data

        if "first_name" in data:
            user.first_name = data["first_name"]

        if "last_name" in data:
            user.last_name = data["last_name"]

        if "username" in data:
            user.username = data["username"]

        if "email" in data:
            user.email = data["email"]

        user.save()

        profile.phone_number = data.get("phone_number", profile.phone_number)
        profile.city = data.get("city", profile.city)
        profile.country = data.get("country", profile.country)
        profile.zip_code = data.get("zip_code", profile.zip_code)
        profile.bio_text = data.get("bio_text", profile.bio_text)
        profile.profile_pic = data.get("profile_pic", profile.profile_pic)
        profile.timezone = data.get("timezone", profile.timezone)
        profile.bio_attachment = data.get("bio_attachment", profile.bio_attachment)
        profile.save()

        return Response(
            {
                "message": "Account settings updated successfully.",
                "user": {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "username": user.username,
                    "email": user.email,
                },
                "profile": {
                    "phone_number": profile.phone_number,
                    "city": profile.city,
                    "country": profile.country,
                    "zip_code": profile.zip_code,
                    "bio": profile.bio_text,
                    "profile_pic": profile.profile_pic if profile.profile_pic else None,
                    "bio_attachment": (
                        profile.bio_attachment.url if profile.bio_attachment else None
                    ),
                    "timezone": profile.timezone,
                },
            },
            status=status.HTTP_200_OK,
        )


class DashboardOverviewView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        cache_key = f"dashboard_overview_{user.id}"
        data = cache.get(cache_key)

        if not data:
           
            rebuild_recommendations_cache.delay(user.id)

            recent = Activity.objects.filter(user=user)[:15]
            recommendations = get_recommended_steps(user)

            data = {
                "recent_activities": ActivitySerializer(recent, many=True).data,
                "recommendations": recommendations,
                "cached": False
            }
            cache.set(cache_key, data, timeout=60 * 30)

        return Response(data)

