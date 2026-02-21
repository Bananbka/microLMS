from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

from apps.users.domain.entities import RoleEntity, UserEntity
from apps.users.infrastructure.models import Role, User, Permission


class RoleRepository:
    def _to_entity(self, role: Role) -> RoleEntity:
        return RoleEntity(
            id=role.id,
            name=role.name,
            slug=role.slug,
            permissions=[p.slug for p in role.permissions.all()]
        )

    def _from_entity(self, role_ent: RoleEntity) -> Role:
        return Role.objects.get(id=role_ent.id)

    def get_default_student_role(self) -> RoleEntity:
        role, _ = Role.objects.get_or_create(
            slug='student',
            defaults={'name': 'Student'}
        )
        return self._to_entity(role)

    def get_all_roles(self) -> list[RoleEntity]:
        roles = Role.objects.prefetch_related('permissions').all()
        return [self._to_entity(role) for role in roles]

    def get_role_by_slug(self, slug: str) -> RoleEntity:
        role = get_object_or_404(Role, slug=slug)
        return self._to_entity(role)

    def create_role(self, name: str, slug: str, permission_slugs: list = None) -> RoleEntity:
        role = Role.objects.create(name=name, slug=slug)
        if permission_slugs:
            perms = Permission.objects.filter(slug__in=permission_slugs)
            role.permissions.set(perms)

        return self._to_entity(role)

    def is_role_exists(self, slug: str) -> bool:
        return Role.objects.filter(slug=slug).exists()


class UserRepository:
    def _to_entity(self, user: User) -> UserEntity:
        return UserEntity(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            phone=user.phone,
            role=user.role.slug if getattr(user, 'role', None) else None
        )

    def _from_entity(self, user: UserEntity) -> User:
        return User.objects.get(id=user.id)

    def create_user(self, email, password, full_name, phone, role) -> UserEntity:
        try:
            user = User.objects.create_user(
                email=email,
                password=password,
                full_name=full_name,
                phone=phone,
                role=role
            )
            return self._to_entity(user)

        except IntegrityError as e:
            error_msg = str(e).lower()
            if 'phone' in error_msg:
                raise ValidationError({"phone": ["User with this phone already exists."]})
            if 'email' in error_msg:
                raise ValidationError({"email": ["This email is already in use."]})
            raise

    def get_all_users(self):
        users = User.objects.select_related('role').all()
        return [self._to_entity(u) for u in users]

    def update_user_role(self, user_ent: UserEntity, role_ent: RoleEntity) -> UserEntity:
        user = self._from_entity(user_ent)
        user.role_id = role_ent.id
        user.save(update_fields=['role_id'])
        user_ent.role = role_ent.slug
        return user_ent

    def get_user_by_id(self, user_id: int) -> UserEntity:
        user = get_object_or_404(User.objects.select_related('role'), id=user_id)
        return self._to_entity(user)

    def update_user(self, user_id: int, update_data: dict) -> UserEntity:
        try:
            user = get_object_or_404(User, id=user_id)

            for key, value in update_data.items():
                setattr(user, key, value)

            user.save()
            return self._to_entity(user)

        except IntegrityError as e:
            error_msg = str(e).lower()
            if 'phone' in error_msg:
                raise ValidationError({"phone": ["User with this phone already exists."]})
            if 'email' in error_msg:
                raise ValidationError({"email": ["This email is already in use."]})
            raise

    def delete_user(self, user_id: int) -> None:
        user = get_object_or_404(User, id=user_id)
        user.delete()
