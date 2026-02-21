from drf_spectacular.extensions import OpenApiAuthenticationExtension
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.utils import translation


class StatelessUser:
    def __init__(self, token_data):
        self.id = token_data.get('user_id')
        self.email = token_data.get('email')
        self.full_name = token_data.get('full_name')
        self.role_slug = token_data.get('role')
        self.is_authenticated = True


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        raw_token = request.COOKIES.get('access-token')

        if not raw_token:
            return None

        try:
            validated_token = self.get_validated_token(raw_token)
        except AuthenticationFailed:
            return None

        user = StatelessUser(validated_token)

        return user, validated_token


class CookieJWTAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = CookieJWTAuthentication
    name = 'cookieAuth'

    def get_security_definition(self, auto_schema):
        return {
            'type': 'apiKey',
            'in': 'cookie',
            'name': 'access-token',
            'description': 'JWT Token in HttpOnly cookie (access-token)'
        }
