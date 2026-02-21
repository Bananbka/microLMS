from ..domain.entities import CourseEntity
from ..infrastructure.repositories import CourseRepository


class CourseService:
    def __init__(self, repository: CourseRepository = None):
        self.repository = repository or CourseRepository()

    def create_course(self, title: str, description: str | None = None) -> CourseEntity:
        course = CourseEntity(title=title, description=description)
        return self.repository.save(course)
