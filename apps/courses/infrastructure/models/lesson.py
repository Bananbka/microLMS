from django.db import models


class Lesson(models.Model):
    topic = models.CharField(max_length=127)
    html_content = models.TextField()

    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='lessons')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author_id = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'courses_lessons'
        ordering = ['-created_at']
