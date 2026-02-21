from django.urls import path, include

from apps.users.controllers.views import RegistrationAPIView, LoginAPIView, LogoutAPIView, RefreshAPIView

auth_urls = [
    path('register/', RegistrationAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('refresh/', RefreshAPIView.as_view(), name='refresh'),

]

urlpatterns = [
    path('auth/', include(auth_urls)),
]
