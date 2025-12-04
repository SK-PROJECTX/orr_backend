from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiExample
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from admin_portal.models import AdminProfile
from client.models import Profile as ClientProfile
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

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
            value={"username": "editor", "password": "editor123"},
            request_only=True
        )
    ]
)
@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    """Login endpoint for content editors"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response(
                {'error': 'Username and password required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = authenticate(username=username, password=password)
        
        if user and user.is_active:
            refresh = RefreshToken.for_user(user)
            
            # Check if user is admin
            try:
                admin_profile = AdminProfile.objects.get(user=user, is_active=True)
                role_name = admin_profile.role.name if admin_profile.role else 'admin'
                
                return Response({
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'is_staff': user.is_staff,
                        'is_superuser': user.is_superuser,
                        'user_type': 'admin',
                        'role': role_name,
                        'can_edit_content': admin_profile.role.can_create_content if admin_profile.role else user.is_superuser,
                        'permissions': {
                            'can_manage_users': admin_profile.role.can_manage_users if admin_profile.role else user.is_superuser,
                            'can_view_all_clients': admin_profile.role.can_view_all_clients if admin_profile.role else user.is_superuser,
                            'can_edit_clients': admin_profile.role.can_edit_clients if admin_profile.role else user.is_superuser,
                            'can_manage_tickets': admin_profile.role.can_manage_tickets if admin_profile.role else user.is_superuser,
                            'can_create_content': admin_profile.role.can_create_content if admin_profile.role else user.is_superuser,
                            'can_publish_content': admin_profile.role.can_publish_content if admin_profile.role else user.is_superuser,
                        }
                    }
                })
                
            except AdminProfile.DoesNotExist:
                # Check if user is client
                try:
                    client_profile = ClientProfile.objects.get(user=user)
                    
                    return Response({
                        'access': str(refresh.access_token),
                        'refresh': str(refresh),
                        'user': {
                            'id': user.id,
                            'username': user.username,
                            'email': user.email,
                            'is_staff': user.is_staff,
                            'is_superuser': user.is_superuser,
                            'user_type': 'client',
                            'role': 'client',
                            'can_edit_content': False,
                            'permissions': {
                                'can_view_own_data': True,
                                'can_book_meetings': True,
                                'can_create_tickets': True,
                                'can_view_content': True,
                            }
                        }
                    })
                    
                except ClientProfile.DoesNotExist:
                    # Django superuser without profiles
                    if user.is_superuser:
                        return Response({
                            'access': str(refresh.access_token),
                            'refresh': str(refresh),
                            'user': {
                                'id': user.id,
                                'username': user.username,
                                'email': user.email,
                                'is_staff': user.is_staff,
                                'is_superuser': user.is_superuser,
                                'user_type': 'admin',
                                'role': 'super_admin',
                                'can_edit_content': True,
                                'permissions': {
                                    'can_manage_users': True,
                                    'can_view_all_clients': True,
                                    'can_edit_clients': True,
                                    'can_manage_tickets': True,
                                    'can_create_content': True,
                                    'can_publish_content': True,
                                }
                            }
                        })
        
        return Response(
            {'error': 'Invalid credentials'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )