from django.urls import path

from apps.courses.controllers.views import CourseAPIView

urlpatterns = [
    path('courses/', CourseAPIView.as_view(), name='courses'),
]
