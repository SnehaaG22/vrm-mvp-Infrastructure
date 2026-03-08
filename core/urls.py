from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from apps.common.views import LoginView, UserProfileView, AssessmentViewSet, VendorViewSet

# Create a router for viewsets
router = DefaultRouter()
router.register(r'assessments', AssessmentViewSet, basename='assessment')
router.register(r'vendors', VendorViewSet, basename='vendor')

urlpatterns = [
    path("admin/", admin.site.urls),
    # API routes
    path("api/auth/login/", LoginView.as_view(), name="api-login"),
    path("api/users/me/", UserProfileView.as_view(), name="api-user-me"),
    path("api/", include(router.urls)),
    path("api/notifications/", include("apps.notifications.urls")),
    path("api/evidence/", include("apps.evidence.urls")),
    path('', include('django_prometheus.urls')),
]
