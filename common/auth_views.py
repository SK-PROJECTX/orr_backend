from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiExample
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.middleware.csrf import get_token
from admin_portal.models import AdminProfile
from client.models import Profile as ClientProfile
from rest_framework import serializers
from client.v1.serializers.auth import LoginSerializer

class LoginResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = serializers.DictField()

@extend_schema(
    tags=["Authentication"],
    summary="Login for content editors",
    description="Authenticate content editors and return JWT tokens",
    request=LoginSerializer,
    responses={200: LoginResponseSerializer},
    examples=[
        OpenApiExample(
            "Login Example",
            value={"email": "editor@example.com", "password": "editor123"},
            request_only=True
        )
    ]
)
@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        role_info = serializer.validated_data["role_info"]

       
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "status": status.HTTP_200_OK,
                "message": "Login successful",
                "data": {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        **role_info,
                    },
                },
            },
            status=status.HTTP_200_OK,)