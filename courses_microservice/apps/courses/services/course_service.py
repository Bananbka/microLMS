from ..infrastructure.repositories import CourseRepository, LessonRepository


class CourseService:
    def __init__(self, course_repo=None):
        self.course_repo = course_repo or CourseRepository()

    def get_all_courses(self):
        return self.course_repo.get_all()

    def get_course(self, course_id: int):
        return self.course_repo.get_by_id(course_id)

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
