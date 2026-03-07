import uuid
import threading
import logging

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