from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication


class CookieJWTAuthentication(JWTAuthentication):

    def authenticate(self, request):
        # Look for the token in cookies
        token = request.COOKIES.get("auth_token")
        if not token:
            return None

        # Validate and authenticate using the parent class
        validated_token = self.get_validated_token(token)
        user = self.get_user(validated_token)
        return (user, validated_token)
