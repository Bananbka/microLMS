from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from core.views import HealthCheckAPIView

urlpatterns = [
    path('v1/courses/', include('apps.courses.controllers.urls')),

    path('health/', HealthCheckAPIView.as_view(), name='health-check'),

    path('admin/', admin.site.urls),

    path('api/courses/doc/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/courses/doc/schema/redoc/', SpectacularRedocView.as_view(url_name="schema", ), name='redoc'),
    path('api/courses/doc/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name="schema"), name='swagger-ui'),

]
