from apps.users.infrastructure.models import Role, User


class RoleRepository:
    def get_default_student_role(self) -> Role:
        role, _ = Role.objects.get_or_create(
            slug='student',
            defaults={'name': 'Student'}
        )
        return role


class UserRepository:
    def create_user(self, email, password, full_name, phone, role) -> User:
        return User.objects.create_user(
            email=email,
            password=password,
            full_name=full_name,
            phone=phone,
            role=role
        )
