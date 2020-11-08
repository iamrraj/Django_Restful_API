from time import time
from rest_framework.response import Response
from django.utils.six.moves.http_client import responses


def error_json_response(request, status_code, message=None, warning=None):
    data = {
        'timestamp': round(time() * 1000),
        'status': status_code,
        'error': responses.get(status_code, 'Unknown Status Code'),
        'path': request.path,
    }
    if message is not None:
        data['message'] = message
    if warning is not None:
        data['warning'] = warning
    response = Response(data, status=status_code)
    response.status_code = status_code
    return response