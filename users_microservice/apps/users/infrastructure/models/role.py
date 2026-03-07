from django.db import models


class Role(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    permissions = models.ManyToManyField(
        'users.Permission',
        blank=True,
        related_name='roles'
    )

    class Meta:
        db_table = 'users_roles'
        ordering = ['name']
