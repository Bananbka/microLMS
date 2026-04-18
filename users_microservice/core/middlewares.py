import uuid
import threading
import logging
import os

import consul
from django.http import JsonResponse

request_local = threading.local()
logger = logging.getLogger(__name__)


class CorrelationIdMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        correlation_id = request.headers.get('X-Correlation-ID')

        if not correlation_id:
            correlation_id = str(uuid.uuid4())

        request.correlation_id = correlation_id
        request_local.correlation_id = correlation_id

        logger.info(f"[{correlation_id}] {request.method} {request.path}")

        response = self.get_response(request)

        response['X-Correlation-ID'] = correlation_id
        return response


def get_current_correlation_id():
    return getattr(request_local, 'correlation_id', str(uuid.uuid4()))


class ConsulMaintenanceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.consul_host = os.environ.get('CONSUL_HOST', 'consul')
        self.c = consul.Consul(host=self.consul_host, port=8500)

    def __call__(self, request):
        try:
            index, data = self.c.kv.get('microlms/users-service/dev/maintenance_mode')
            if data and 'Value' in data:
                maintenance = data['Value'].decode('utf-8').lower()

                if maintenance == 'true':
                    return JsonResponse({
                        "status": "error",
                        "detail": "Service in maintenance mode. Try again later."
                    }, status=503)
        except Exception as e:
            print(f"errorrr: {e}")

        response = self.get_response(request)
        return response
