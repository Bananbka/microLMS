from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from core.permissions import HasPermission

from .serializers import (
    CourseResponseDTO, CourseCreateUpdateDTO,
    LessonResponseDTO, LessonCreateUpdateDTO
)
from ..services.course_service import CourseService, LessonService


### COURSES

class CourseListCreateAPIView(APIView):
    permission_classes = [HasPermission]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.course_service = CourseService()

    def get_required_permissions(self, request):
        if request.method == 'GET':
            return ['courses.read']
        return ['courses.create']

    @extend_schema(tags=["Courses/Courses"], responses=CourseResponseDTO(many=True))
    def get(self, request):
        courses = self.course_service.get_all_courses()
        output_dto = CourseResponseDTO(courses, many=True)
        return Response(output_dto.data)

    @extend_schema(tags=["Courses/Courses"], request=CourseCreateUpdateDTO, responses=CourseResponseDTO)
    def post(self, request):
        input_dto = CourseCreateUpdateDTO(data=request.data)
        input_dto.is_valid(raise_exception=True)

        # Передаємо request.user.id як автора!
        course = self.course_service.create_course(
            data=input_dto.validated_data,
            author_id=request.user.id
        )

        output_dto = CourseResponseDTO(course)
        return Response(output_dto.data, status=201)


class CourseDetailAPIView(APIView):
    permission_classes = [HasPermission]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.course_service = CourseService()

    def get_required_permissions(self, request):
        if request.method == 'GET':
            return ['courses.read']
        if request.method in ['PUT', 'PATCH']:
            return ['courses.edit']
        return ['courses.delete']

    @extend_schema(tags=["Courses/Courses"], responses=CourseResponseDTO)
    def get(self, request, course_id):
        course = self.course_service.get_course(course_id)
        output_dto = CourseResponseDTO(course)
        return Response(output_dto.data)

    @extend_schema(tags=["Courses/Courses"], request=CourseCreateUpdateDTO, responses=CourseResponseDTO)
    def patch(self, request, course_id):
        input_dto = CourseCreateUpdateDTO(data=request.data)
        input_dto.is_valid(raise_exception=True)

        course = self.course_service.update_course(course_id, input_dto.validated_data)
        output_dto = CourseResponseDTO(course)
        return Response(output_dto.data)

    @extend_schema(tags=["Courses/Courses"], responses={204: None})
    def delete(self, request, course_id):
        self.course_service.delete_course(course_id)
        return Response(status=204)


# LESSONS
class LessonListCreateAPIView(APIView):
    permission_classes = [HasPermission]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lesson_service = LessonService()

    def get_required_permissions(self, request):
        if request.method == 'POST':
            return ['courses.edit']
        return ['courses.read']

    @extend_schema(tags=["Courses/Lessons"], request=LessonCreateUpdateDTO, responses=LessonResponseDTO)
    def post(self, request, course_id):
        input_dto = LessonCreateUpdateDTO(data=request.data)
        input_dto.is_valid(raise_exception=True)

        lesson = self.lesson_service.create_lesson(
            course_id=course_id,
            data=input_dto.validated_data,
            author_id=request.user.id
        )

        output_dto = LessonResponseDTO(lesson)
        return Response(output_dto.data, status=201)


class LessonListAPIView(APIView):
    permission_classes = [HasPermission]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lesson_service = LessonService()

    def get_required_permissions(self, request):
        return ['courses.read']

    @extend_schema(tags=["Courses/Lessons"], responses=LessonResponseDTO)
    def get(self, request):
        lessons = self.lesson_service.get_all_lessons()
        output_dto = LessonResponseDTO(lessons, many=True)
        return Response(output_dto.data, status=200)


class LessonDetailAPIView(APIView):
    permission_classes = [HasPermission]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lesson_service = LessonService()

    def get_required_permissions(self, request):
        if request.method in ['PUT', 'PATCH']:
            return ['courses.edit']
        return ['courses.delete']

    @extend_schema(tags=["Courses/Lessons"], responses=LessonResponseDTO)
    def get(self, request, lesson_id):
        lesson = self.lesson_service.get_lesson(lesson_id)
        output_dto = LessonResponseDTO(lesson)
        return Response(output_dto.data, status=200)

    @extend_schema(tags=["Courses/Lessons"], request=LessonCreateUpdateDTO, responses=LessonResponseDTO)
    def patch(self, request, lesson_id):
        input_dto = LessonCreateUpdateDTO(data=request.data)
        input_dto.is_valid(raise_exception=True)

        lesson = self.lesson_service.update_lesson(lesson_id, input_dto.validated_data)
        output_dto = LessonResponseDTO(lesson)
        return Response(output_dto.data)

    @extend_schema(tags=["Courses/Lessons"], responses={204: None})
    def delete(self, request, lesson_id):
        self.lesson_service.delete_lesson(lesson_id)
        return Response(status=204)
