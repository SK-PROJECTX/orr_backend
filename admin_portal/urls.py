from django.urls import path, include

urlpatterns = [
    path('v1/', include('admin_portal.v1.urls')),
]