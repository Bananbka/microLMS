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

    def get_role(self, slug: str):
        return self.role_repo.get_role_by_slug(slug)

    def update_role(self, slug: str, update_data: dict, permission_slugs: list = None):
        return self.role_repo.update_role(slug, update_data, permission_slugs)

    def delete_role(self, slug: str):
        if slug in ['admin', 'student']:
            raise ValidationError({"detail": f"System role '{slug}' cannot be deleted."})

        self.role_repo.delete_role(slug)
