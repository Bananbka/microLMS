from typing import Optional

from django.forms import model_to_dict

from ..domain.entities import CourseEntity
from .models import Course


class CourseRepository:
    def save(self, course: CourseEntity) -> CourseEntity:
        model_instance, created = Course.objects.update_or_create(
            id=course.id,
            defaults={
                'title': course.title,
                'description': course.description,
            }
        )
        course.id = model_instance.id
        return course

    def get_by_id(self, course_id: int) -> Optional[CourseEntity]:
        try:
            instance = Course.objects.get(id=course_id)
            return CourseEntity(**model_to_dict(instance))
        except Course.DoesNotExist:
            return None
