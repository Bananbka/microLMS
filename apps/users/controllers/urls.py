from django.urls import path, include

from apps.users.controllers.views import RegistrationAPIView, LoginAPIView, LogoutAPIView, RefreshAPIView, \
    RoleListCreateAPIView, UserListAPIView, UserAssignRoleAPIView, UserDetailAPIView

auth_urls = [
    path('register/', RegistrationAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('refresh/', RefreshAPIView.as_view(), name='refresh'),

]
users_urls = [
    path('', UserListAPIView.as_view(), name='user-list'),
    path('<int:user_id>/assign-role/', UserAssignRoleAPIView.as_view(), name='user-assign-role'),
    path('<int:user_id>/', UserDetailAPIView.as_view(), name='user-detail'),
]

roles_urls = [
    path('', RoleListCreateAPIView.as_view(), name='role-list-create'),

]

urlpatterns = [
    path('auth/', include(auth_urls)),
    path('users/', include(users_urls)),
    path('roles/', include(roles_urls)),
]
