from rest_framework.views import exception_handler
from datetime import datetime


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        custom_response_data = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'status_code': response.status_code,
            'path': context['request'].path,
            'details': response.data
        }
        response.data = custom_response_data

    return response
