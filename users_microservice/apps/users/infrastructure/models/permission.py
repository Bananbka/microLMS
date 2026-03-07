from django.db import models


class Permission(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    description = models.TextField()

    class Meta:
        db_table = 'users_permissions'
        ordering = ['-name']
