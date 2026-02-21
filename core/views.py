from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema
from django.db import connection
from django.db.utils import OperationalError


class HealthCheckAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(tags=['System'], summary="Перевірка стану сервісу")
    def get(self, request):
        db_status = "ok"
        try:
            connection.ensure_connection()
        except OperationalError:
            db_status = "error"

        status_code = 200 if db_status == "ok" else 503

        return Response(
            {
                "status": "ok" if db_status == "ok" else "degraded",
                "database": db_status,
                "version": "1.0.0"
            },
            status=status_code
        )
