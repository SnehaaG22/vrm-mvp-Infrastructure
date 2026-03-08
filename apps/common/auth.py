from rest_framework.authentication import TokenAuthentication, BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
import re

User = get_user_model()

class DevTokenAuthentication(BaseAuthentication):
    """
    Custom authentication for dev-token format: dev-token-<user_id>
    Used during development. Replace with JWT for production.
    """

    def authenticate(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION', '').split()
        
        if not auth or auth[0].lower() != 'bearer':
            return None
        
        if len(auth) == 1:
            raise AuthenticationFailed('Invalid token header. No credentials provided.')
        
        if len(auth) > 2:
            raise AuthenticationFailed('Invalid token header. Token string should not contain spaces.')

        try:
            token = auth[1]
        except IndexError:
            raise AuthenticationFailed('Invalid token header. Credentials not provided.')

        # Check if it's a dev token
        if token.startswith('dev-token-'):
            # Extract user ID from dev-token-<id>
            match = re.match(r'dev-token-(\d+)', token)
            if match:
                user_id = int(match.group(1))
                try:
                    user = User.objects.get(id=user_id)
                    return (user, token)
                except User.DoesNotExist:
                    raise AuthenticationFailed('Invalid user in dev token.')
        
        raise AuthenticationFailed('Invalid token format.')
