from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['role'] = user.role.slug if user.role else None
        token['full_name'] = user.full_name
        token['email'] = user.email

        if user.role:
            token['permissions'] = list(user.role.permissions.values_list('slug', flat=True))
        else:
            token['permissions'] = []

        return token


### AUTH
class RegistrationDTO(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8)
    full_name = serializers.CharField(max_length=255)
    phone = serializers.CharField(max_length=25)


class UserResponseDTO(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(read_only=True)
    full_name = serializers.CharField(read_only=True)
    phone = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)


class LoginDTO(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8)


### ROLES
class RoleResponseDTO(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    slug = serializers.CharField(read_only=True)
    permissions = serializers.ListField(
        child=serializers.CharField(), read_only=True
    )


class RoleCreateUpdateDTO(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    slug = serializers.SlugField(max_length=255)
    permission_slugs = serializers.ListField(
        child=serializers.CharField(), required=False, write_only=True
    )


class AssignRoleDTO(serializers.Serializer):
    role_slug = serializers.SlugField()


### USERS
class UserUpdateDTO(serializers.Serializer):
    full_name = serializers.CharField(max_length=255, required=False)
    phone = serializers.CharField(max_length=25, required=False)
    email = serializers.EmailField(required=False)
