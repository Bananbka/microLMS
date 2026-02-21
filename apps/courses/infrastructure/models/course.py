from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author_id = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'courses_course'
        ordering = ['-created_at']
