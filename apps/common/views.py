from django.contrib.auth import authenticate, get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

User = get_user_model()


class LoginView(APIView):
    """Simple development login endpoint.

    Accepts POST {email, password} and returns a stub token and user info.
    This is a minimal dev implementation to unblock the frontend. Replace
    with a secure token (JWT or DRF TokenAuth) in production.
    """

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"error": "email and password required"}, status=status.HTTP_400_BAD_REQUEST)

        # Try authenticate using username or email
        user = authenticate(request, username=email, password=password)

        # If not found, try email field lookup if username auth fails
        if user is None:
            try:
                user_obj = User.objects.get(email=email)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

        if user is None:
            return Response({"error": "invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        # Create a simple dev token. For production, return JWT or DRF token.
        token = f"dev-token-{user.id}"

        user_data = {
            "id": user.id,
            "email": user.email,
            "first_name": getattr(user, 'first_name', ''),
            "last_name": getattr(user, 'last_name', ''),
            "org_id": getattr(user, 'org_id', None) or None,
            "is_staff": user.is_staff,
        }

        return Response({"token": token, "user": user_data}, status=status.HTTP_200_OK)


class UserProfileView(APIView):
    """Return basic profile for authenticated user.

    This view uses the presence of the dev token for dev auth: token starting
    with 'dev-token-' will be accepted. For production, wire up proper auth.
    """

    def get(self, request):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

        token = auth_header.split(" ", 1)[1]
        if not token.startswith("dev-token-"):
            return Response({"detail": "Invalid token."}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            user_id = int(token.split("dev-token-")[1])
            user = User.objects.get(id=user_id)
        except Exception:
            return Response({"detail": "Invalid token."}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({
            "id": user.id,
            "email": user.email,
            "first_name": getattr(user, 'first_name', ''),
            "last_name": getattr(user, 'last_name', ''),
            "org_id": getattr(user, 'org_id', None) or None,
            "is_staff": user.is_staff,
        })


# Import ViewSets from models
from .models import AssessmentViewSet, VendorViewSet
