from django.urls import path

from apps.users.controllers.views import RegistrationAPIView

urlpatterns = [
    path('auth/register/', RegistrationAPIView.as_view(), name='register'),
]
