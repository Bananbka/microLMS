from django.urls import path
from .views import CourseListCreateAPIView, CourseDetailAPIView, LessonListCreateAPIView, LessonDetailAPIView, \
    LessonListAPIView

urlpatterns = [
    path('', CourseListCreateAPIView.as_view(), name='course-list-create'),
    path('<int:course_id>/', CourseDetailAPIView.as_view(), name='course-detail'),

    path('lessons/', LessonListAPIView.as_view(), name='lesson-list'),
    path('<int:course_id>/lessons/', LessonListCreateAPIView.as_view(), name='lesson-list-create'),
    path('lessons/<int:lesson_id>/', LessonDetailAPIView.as_view(), name='lesson-detail'),
]
