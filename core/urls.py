from django.contrib import admin
from django.urls import include, path
from apps.common.views import LoginView, UserProfileView

urlpatterns = [
    path("admin/", admin.site.urls),
    # API routes
    path("api/auth/login/", LoginView.as_view(), name="api-login"),
    path("api/users/me/", UserProfileView.as_view(), name="api-user-me"),
    path("api/notifications/", include("apps.notifications.urls")),
    path("api/evidence/", include("apps.evidence.urls")),
]
