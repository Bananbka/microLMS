from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import CourseDTO
from ..services.course_service import CourseService


@extend_schema(tags=["Courses/Course"], request=CourseDTO)
class CourseAPIView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = CourseService()

    def post(self, request):
        input_dto = CourseDTO(data=request.data)
        input_dto.is_valid(raise_exception=True)
        data = input_dto.validated_data

        course_entity = self.service.create_course(**data)

        output_dto = CourseDTO(instance=course_entity)
        return Response(output_dto.data, status=status.HTTP_201_CREATED)
