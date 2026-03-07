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

    def get_all_users(self):
        return self.user_repo.get_all_users()

    def assign_role_to_user(self, user_id: int, role_slug: str):
        user = self.user_repo.get_user_by_id(user_id)
        role = self.role_repo.get_role_by_slug(role_slug)
        updated_user = self.user_repo.update_user_role(user, role)
        return updated_user

    def get_user(self, user_id: int):
        return self.user_repo.get_user_by_id(user_id)

    def update_user(self, user_id: int, update_data: dict):
        return self.user_repo.update_user(user_id, update_data)

    def delete_user(self, user_id: int):
        self.user_repo.delete_user(user_id)
