from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('courses/', include('apps.courses.controllers.urls')),
    path('users/', include('apps.users.controllers.urls')),
    path('payroll/', include('apps.payroll.controllers.urls')),

    path('admin/', admin.site.urls),

    path('doc/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('doc/schema/redoc/', SpectacularRedocView.as_view(url_name="schema", ), name='redoc'),
    path('doc/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name="schema"), name='swagger-ui'),

]
