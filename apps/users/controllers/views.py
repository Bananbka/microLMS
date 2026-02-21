from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema

from .serializers import RegistrationDTO, UserResponseDTO, CustomTokenObtainPairSerializer
from .utils import set_auth_cookies
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
