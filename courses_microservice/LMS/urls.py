from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from core.views import HealthCheckAPIView

urlpatterns = [
    path('v1/courses/', include('apps.courses.controllers.urls')),
    path('v1/users/', include('apps.users.controllers.urls')),
    path('v1/payroll/', include('apps.payroll.controllers.urls')),

    path('health/', HealthCheckAPIView.as_view(), name='health-check'),

    path('admin/', admin.site.urls),

    path('doc/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('doc/schema/redoc/', SpectacularRedocView.as_view(url_name="schema", ), name='redoc'),
    path('doc/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name="schema"), name='swagger-ui'),

]
