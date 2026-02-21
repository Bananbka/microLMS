from apps.users.infrastructure.repository import UserRepository, RoleRepository


class UserService:
    def __init__(self, user_repo: UserRepository = None, role_repo: RoleRepository = None):
        self.user_repo = user_repo or UserRepository()
        self.role_repo = role_repo or RoleRepository()

    def register_user(self, email, password, full_name, phone):
        student_role = self.role_repo.get_default_student_role()

        user = self.user_repo.create_user(
            email=email,
            password=password,
            full_name=full_name,
            phone=phone,
            role=student_role
        )

        return user
