from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer


class AuthService:

    @staticmethod
    def authenticate_user(email, password):
        user = authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed("Invalid credentials")

        if not user.is_active:
            raise AuthenticationFailed("User is blocked")

        return user

    @staticmethod
    def refresh_tokens(refresh_token: str) -> tuple[str, str]:
        try:
            serializer = TokenRefreshSerializer(data={'refresh': refresh_token})
            serializer.is_valid(raise_exception=True)
        except (TokenError, InvalidToken):
            raise AuthenticationFailed("Недійсний або прострочений refresh token.")

        new_access = serializer.validated_data.get('access')
        new_refresh = serializer.validated_data.get('refresh', refresh_token)

        return new_access, new_refresh
