from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from core.views import HealthCheckAPIView

urlpatterns = [
    path('v1/payroll/', include('apps.payroll.controllers.urls')),

    path('health/', HealthCheckAPIView.as_view(), name='health-check'),

    path('admin/', admin.site.urls),

    path('api/payroll/doc/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/payroll/doc/schema/redoc/', SpectacularRedocView.as_view(url_name="schema", ), name='redoc'),
    path('api/payroll/doc/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name="schema"), name='swagger-ui'),

]
