from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from LMS import settings
from .serializers import RegistrationDTO, UserResponseDTO, CustomTokenObtainPairSerializer, LoginDTO
from .utils import set_auth_cookies
from ..services.auth_service import AuthService
from ..services.user_service import UserService


class RegistrationAPIView(APIView):
    permission_classes = [AllowAny]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_service = UserService()

    @extend_schema(tags=['Users/Authentication'], request=RegistrationDTO, responses=UserResponseDTO)
    def post(self, request):
        input_dto = RegistrationDTO(data=request.data)
        input_dto.is_valid(raise_exception=True)
        data = input_dto.data

        user = self.user_service.register_user(**data)

        refresh = CustomTokenObtainPairSerializer.get_token(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        output_dto = UserResponseDTO(instance=user)
        resp = Response(output_dto.data, status=201)

        set_auth_cookies(resp, access_token, refresh_token)

        return resp


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.auth_service = AuthService()

    @extend_schema(tags=['Users/Authentication'], request=LoginDTO, responses=UserResponseDTO)
    def post(self, request):
        input_dto = LoginDTO(data=request.data)
        input_dto.is_valid(raise_exception=True)
        data = input_dto.data

        user = self.auth_service.authenticate_user(**data)

        refresh = CustomTokenObtainPairSerializer.get_token(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        output_dto = UserResponseDTO(instance=user)
        resp = Response(output_dto.data, status=200)

        set_auth_cookies(resp, access_token, refresh_token)
        return resp


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(tags=['Users/Authentication'])
    def post(self, request):
        resp = Response({"message": "Successfully logged out."}, status=200)
        resp.delete_cookie('access-token')
        resp.delete_cookie('refresh-token')
        return resp


class RefreshAPIView(APIView):
    permission_classes = [AllowAny]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.auth_service = AuthService()

    @extend_schema(tags=['Users/Authentication'])
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh-token')

        if not refresh_token:
            return Response(
                {"message": "Refresh token is missing in cookies."},
                status=401
            )

        new_access, new_refresh = self.auth_service.refresh_tokens(refresh_token)
        resp = Response({"message": "Токени успішно оновлено."}, status=200)
        set_auth_cookies(resp, new_access, new_refresh)
        return resp
