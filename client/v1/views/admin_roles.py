from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from admin_portal.models import AdminRole


@extend_schema(
    tags=["Authentication"],
    summary="Get available admin roles for registration",
    description="Retrieve list of available admin roles for user registration.",
)
class AdminRolesView(APIView):
    """Get available admin roles for registration"""

    permission_classes = [AllowAny]

    def get(self, request):
        roles = AdminRole.objects.all().values("id", "name", "description")
        return Response(
            {
                "roles": [
                    {
                        "value": role["name"],
                        "label": dict(AdminRole.ROLE_CHOICES).get(
                            role["name"], role["name"]
                        ),
                        "description": role["description"],
                    }
                    for role in roles
                ]
            }
        )
