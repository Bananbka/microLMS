from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('full_name', 'Super Admin')

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')

        from .role import Role

        admin_role, created = Role.objects.get_or_create(
            slug='admin',
            defaults={'name': 'Admin'}
        )
        extra_fields['role'] = admin_role

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)

    date_of_birth = models.DateField(null=True, blank=True)

    phone = models.CharField(max_length=25, unique=True)

    role = models.ForeignKey(
        'users.Role',
        on_delete=models.PROTECT,
        related_name='users',
        null=True
    )

    supervisor = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'role']
    first_name, last_name, username = (None,) * 3
    objects = CustomUserManager()

    class Meta:
        db_table = 'users_users'
        ordering = ['-date_joined']


    def has_permission(self, perm_slug):
        if self.is_superuser: return True
        if not self.role: return False
        return self.role.permissions.filter(slug=perm_slug).exists()
