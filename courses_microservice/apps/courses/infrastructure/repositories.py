from django.shortcuts import get_object_or_404

from .models.couese_purchase import PurchaseStatus
from ..domain.entities import CourseEntity, LessonEntity, CoursePurchaseEntity
from .models import Course, Lesson, CoursePurchase


class CourseRepository:
    def _lesson_to_entity(self, lesson: Lesson) -> LessonEntity:
        return LessonEntity(
            id=lesson.id,
            topic=lesson.topic,
            html_content=lesson.html_content,
            course_id=lesson.course_id,
            author_id=lesson.author_id,
            created_at=lesson.created_at,
            updated_at=lesson.updated_at
        )

    def _course_to_entity(self, course: Course) -> CourseEntity:
        return CourseEntity(
            id=course.id,
            title=course.title,
            description=course.description,
            is_active=course.is_active,
            author_id=course.author_id,
            created_at=course.created_at,
            updated_at=course.updated_at,
            lessons=[self._lesson_to_entity(l) for l in course.lessons.all()]
        )

    def get_all(self) -> list[CourseEntity]:
        courses = Course.objects.prefetch_related('lessons').all()
        return [self._course_to_entity(c) for c in courses]

    def get_by_id(self, course_id: int) -> CourseEntity:
        course = get_object_or_404(Course.objects.prefetch_related('lessons'), id=course_id)
        return self._course_to_entity(course)

    def create(self, title: str, description: str = None, author_id: int = None) -> CourseEntity:
        course = Course.objects.create(
            title=title,
            description=description,
            author_id=author_id
        )
        return self._course_to_entity(course)

    def update(self, course_id: int, update_data: dict) -> CourseEntity:
        course = get_object_or_404(Course, id=course_id)

        for key, value in update_data.items():
            setattr(course, key, value)

        course.save()
        return self._course_to_entity(course)

    def delete(self, course_id: int) -> None:
        course = get_object_or_404(Course, id=course_id)
        course.delete()


class LessonRepository:
    def _to_entity(self, lesson: Lesson) -> LessonEntity:
        return LessonEntity(
            id=lesson.id,
            topic=lesson.topic,
            html_content=lesson.html_content,
            course_id=lesson.course_id,
            author_id=lesson.author_id,
            created_at=lesson.created_at,
            updated_at=lesson.updated_at
        )

    def get_by_id(self, lesson_id: int) -> LessonEntity:
        lesson = get_object_or_404(Lesson, id=lesson_id)
        return self._to_entity(lesson)

    def get_all(self) -> list[LessonEntity]:
        lessons = Lesson.objects.all()
        return [self._to_entity(l) for l in lessons]

    def create(self, course_id: int, topic: str, html_content: str, author_id: int = None) -> LessonEntity:
        lesson = Lesson.objects.create(
            course_id=course_id,
            topic=topic,
            html_content=html_content,
            author_id=author_id
        )
        return self._to_entity(lesson)

    def update(self, lesson_id: int, update_data: dict) -> LessonEntity:
        lesson = get_object_or_404(Lesson, id=lesson_id)

        for key, value in update_data.items():
            setattr(lesson, key, value)

        lesson.save()
        return self._to_entity(lesson)

    def delete(self, lesson_id: int) -> None:
        lesson = get_object_or_404(Lesson, id=lesson_id)
        lesson.delete()


class CoursePurchaseRepository:
    def _to_entity(self, course_purchase: CoursePurchase) -> CoursePurchaseEntity:
        return CoursePurchaseEntity(
            id=course_purchase.id,
            user_id=course_purchase.user_id,
            course=course_purchase.course.id,
            price_at_moment=course_purchase.price_at_moment,
            status=course_purchase.status,
            error_message=course_purchase.error_message,
            created_at=course_purchase.created_at,
            updated_at=course_purchase.updated_at
        )

    def create(self, **kwargs) -> CoursePurchaseEntity:
        kwargs['status'] = 'PENDING'
        course_purchase = CoursePurchase.objects.create(**kwargs)
        return self._to_entity(course_purchase)

    def get_by_id(self, id_: int) -> CoursePurchaseEntity:
        course_purchase = get_object_or_404(CoursePurchase, id=id_)
        return self._to_entity(course_purchase)

    def get_all(self) -> list[CoursePurchaseEntity]:
        course_purchases = CoursePurchase.objects.all()
        return [self._to_entity(cp) for cp in course_purchases]
