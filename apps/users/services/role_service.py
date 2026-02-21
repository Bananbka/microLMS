from rest_framework.exceptions import ValidationError

from apps.users.infrastructure.repository import RoleRepository


class RoleService:
    def __init__(self, role_repo=None):
        self.role_repo = role_repo or RoleRepository()

    def get_all_roles(self):
        return self.role_repo.get_all_roles()

    def create_role(self, name: str, slug: str, permission_slugs: list = None):
        if self.role_repo.is_role_exists(slug):
            raise ValidationError('Role already exists')
        return self.role_repo.create_role(name, slug, permission_slugs)
