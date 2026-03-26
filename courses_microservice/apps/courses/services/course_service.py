import pybreaker
import requests

from ..domain.entities import CoursePurchaseEntity
from ..infrastructure.http_clients import fetch_author_data
from ..infrastructure.models import OutboxEvent
from ..infrastructure.repositories import CourseRepository, LessonRepository, CoursePurchaseRepository


class CourseService:
    def __init__(self, course_repo=None):
        self.course_repo = course_repo or CourseRepository()
        self.course_pur_repo = CoursePurchaseRepository()

    def get_all_courses(self):
        return self.course_repo.get_all()

    def get_course(self, course_id: int, cookies: dict = None):
        course = self.course_repo.get_by_id(course_id)

        author_data = None
        if course.author_id:
            try:
                user_response = fetch_author_data(course.author_id, cookies=cookies)
                author_data = {
                    "id": user_response.get("id"),
                    "first_name": user_response.get("first_name"),
                    "last_name": user_response.get("last_name"),
                    "email": user_response.get("email")
                }
            except pybreaker.CircuitBreakerError:
                author_data = {"id": course.author_id, "first_name": "Service currently", "last_name": "unavailable"}
            except requests.exceptions.RequestException:
                author_data = {"id": course.author_id, "first_name": "Unknown", "last_name": "Author"}

        return {
            "id": course.id,
            "title": course.title,
            "description": course.description,
            "author": author_data,
            "price": course.price
        }

    def create_course(self, data: dict, author_id: int):
        return self.course_repo.create(
            title=data['title'],
            description=data.get('description'),
            author_id=author_id
        )

    def update_course(self, course_id: int, update_data: dict):
        return self.course_repo.update(course_id, update_data)

    def delete_course(self, course_id: int):
        self.course_repo.delete(course_id)

    def purchase_course(self, course_id: int, user_id: int):
        course = self.get_course(course_id)

        purchase = self.course_pur_repo.create(
            user_id=user_id,
            course_id=course['id'],
            price_at_moment=course['price']
        )

        OutboxEvent.objects.create(
            event_type='CoursePurchaseInitiated',
            routing_key='course.purchase.initiated',
            payload={
                "purchase_id": purchase.id,
                "user_id": user_id,
                "course_id": course['id'],
                "author_id": course['author']['id'],
                "price": str(course['price'])
            }
        )
        return purchase


class LessonService:
    def __init__(self, lesson_repo=None, course_repo=None):
        self.lesson_repo = lesson_repo or LessonRepository()
        self.course_repo = course_repo or CourseRepository()

    def get_lesson(self, lesson_id: int):
        return self.lesson_repo.get_by_id(lesson_id)

    def get_all_lessons(self):
        return self.lesson_repo.get_all()

    def create_lesson(self, course_id: int, data: dict, author_id: int):
        self.course_repo.get_by_id(course_id)

        return self.lesson_repo.create(
            course_id=course_id,
            topic=data['topic'],
            html_content=data['html_content'],
            author_id=author_id
        )

    def update_lesson(self, lesson_id: int, update_data: dict):
        return self.lesson_repo.update(lesson_id, update_data)

    def delete_lesson(self, lesson_id: int):
        self.lesson_repo.delete(lesson_id)
