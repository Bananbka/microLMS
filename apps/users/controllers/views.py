from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_spectacular.utils import extend_schema

from core.permissions import HasPermission
from .serializers import RegistrationDTO, UserResponseDTO, CustomTokenObtainPairSerializer, LoginDTO, RoleResponseDTO, \
    RoleCreateUpdateDTO, AssignRoleDTO, UserUpdateDTO, RoleUpdateDTO
from .utils import set_auth_cookies
from ..services.auth_service import AuthService
from ..services.role_service import RoleService
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


### ROLES
class RoleListCreateAPIView(APIView):
    permission_classes = [HasPermission]
    required_permissions = ['roles.manage']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.role_service = RoleService()

    @extend_schema(tags=['Users/Roles'], responses=RoleResponseDTO(many=True))
    def get(self, request):
        roles = self.role_service.get_all_roles()
        output_dto = RoleResponseDTO(roles, many=True)
        return Response(output_dto.data)

    @extend_schema(tags=['Users/Roles'], request=RoleCreateUpdateDTO, responses=RoleResponseDTO)
    def post(self, request):
        input_dto = RoleCreateUpdateDTO(data=request.data)
        input_dto.is_valid(raise_exception=True)

        role = self.role_service.create_role(
            name=input_dto.validated_data['name'],
            slug=input_dto.validated_data['slug'],
            permission_slugs=input_dto.validated_data.get('permission_slugs', [])
        )

        output_dto = RoleResponseDTO(role)
        return Response(output_dto.data, status=201)


class RoleDetailAPIView(APIView):
    permission_classes = [HasPermission]
    required_permissions = ['roles.manage']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.role_service = RoleService()

    @extend_schema(tags=['Users/Roles'], responses=RoleResponseDTO)
    def get(self, request, slug):
        role_entity = self.role_service.get_role(slug)
        output_dto = RoleResponseDTO(role_entity)
        return Response(output_dto.data)

    @extend_schema(tags=['Users/Roles'], request=RoleUpdateDTO, responses=RoleResponseDTO)
    def patch(self, request, slug):
        input_dto = RoleUpdateDTO(data=request.data)
        input_dto.is_valid(raise_exception=True)

        data = input_dto.validated_data
        permission_slugs = data.pop('permission_slugs', None)

        updated_role_entity = self.role_service.update_role(
            slug=slug,
            update_data=data,
            permission_slugs=permission_slugs
        )

        output_dto = RoleResponseDTO(updated_role_entity)
        return Response(output_dto.data)

    @extend_schema(tags=['Users/Roles'], responses={204: None})
    def delete(self, request, slug):
        self.role_service.delete_role(slug)
        return Response(status=204)


### USERS
class UserListAPIView(APIView):
    permission_classes = [HasPermission]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_service = UserService()

    def get_required_permissions(self, request):
        if request.method == 'GET':
            return ['users.read']
        return ['users.create']

    @extend_schema(tags=['Users/Users'], responses=UserResponseDTO(many=True))
    def get(self, request):
        users = self.user_service.get_all_users()
        output_dto = UserResponseDTO(users, many=True)
        return Response(output_dto.data)

    @extend_schema(tags=['Users/Users'], request=RegistrationDTO, responses=UserResponseDTO)
    def post(self, request):
        input_dto = RegistrationDTO(data=request.data)
        input_dto.is_valid(raise_exception=True)
        data = input_dto.data
        user_ent = self.user_service.register_user(**data)

        output_dto = UserResponseDTO(instance=user_ent)
        return Response(output_dto.data, status=201)


class UserDetailAPIView(APIView):
    permission_classes = [HasPermission]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_service = UserService()

    def get_required_permissions(self, request):
        if request.method == 'GET':
            return ['users.read']
        elif request.method in ['PUT', 'PATCH']:
            return ['users.edit']
        elif request.method == 'DELETE':
            return ['users.delete']
        return []

    @extend_schema(tags=['Users/Users'], responses=UserResponseDTO)
    def get(self, request, user_id):
        user_entity = self.user_service.get_user(user_id)
        output_dto = UserResponseDTO(user_entity)
        return Response(output_dto.data)

    @extend_schema(tags=['Users/Users'], request=UserUpdateDTO, responses=UserResponseDTO)
    def patch(self, request, user_id):
        input_dto = UserUpdateDTO(data=request.data)
        input_dto.is_valid(raise_exception=True)

        updated_user_entity = self.user_service.update_user(
            user_id=user_id,
            update_data=input_dto.validated_data
        )

        output_dto = UserResponseDTO(updated_user_entity)
        return Response(output_dto.data)

    @extend_schema(tags=['Users/Users'], responses={204: None})
    def delete(self, request, user_id):
        self.user_service.delete_user(user_id)
        return Response(status=204)


class UserAssignRoleAPIView(APIView):
    permission_classes = [HasPermission]
    required_permissions = ['users.assign_role']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_service = UserService()

    @extend_schema(tags=['Users/Users'], request=AssignRoleDTO, responses=UserResponseDTO)
    def post(self, request, user_id):
        input_dto = AssignRoleDTO(data=request.data)
        input_dto.is_valid(raise_exception=True)

        updated_user = self.user_service.assign_role_to_user(
            user_id=user_id,
            role_slug=input_dto.validated_data['role_slug']
        )

        output_dto = UserResponseDTO(updated_user)
        return Response(output_dto.data, status=200)
