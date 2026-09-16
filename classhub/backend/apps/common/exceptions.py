"""
ClassHub Common Exceptions
"""
from rest_framework.views import exception_handler
from rest_framework.exceptions import (
    APIException,
    PermissionDenied,
    NotFound,
    AuthenticationFailed,
    Throttled,
)
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """Custom exception handler for DRF."""
    response = exception_handler(exc, context)
    
    if response is not None:
        # Add custom error format
        error_data = {
            'error': {
                'status_code': response.status_code,
                'message': get_error_message(response),
                'details': response.data if isinstance(response.data, dict) else {'detail': response.data},
            }
        }
        response.data = error_data
    else:
        # Handle uncaught exceptions
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        response = Response(
            {
                'error': {
                    'status_code': 500,
                    'message': 'Internal server error',
                    'details': {'error': str(exc)} if context.get('request').user.is_staff else {}
                }
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    return response


def get_error_message(response):
    """Get appropriate error message based on status code."""
    status_messages = {
        400: 'Bad request',
        401: 'Authentication required',
        403: 'Permission denied',
        404: 'Resource not found',
        405: 'Method not allowed',
        408: 'Request timeout',
        409: 'Conflict',
        413: 'Payload too large',
        415: 'Unsupported media type',
        429: 'Too many requests',
        500: 'Internal server error',
        502: 'Bad gateway',
        503: 'Service unavailable',
        504: 'Gateway timeout',
    }
    
    return status_messages.get(response.status_code, 'An error occurred')


class ClassHubException(APIException):
    """Base exception for ClassHub application."""
    
    status_code = 400
    default_detail = 'An error occurred'
    
    def __init__(self, detail=None, code=None):
        if detail is not None:
            self.detail = detail
        else:
            self.detail = self.default_detail
        if code is not None:
            self.status_code = code


class ValidationError(ClassHubException):
    """Validation error."""
    
    default_detail = 'Validation error'


class NotFoundError(ClassHubException):
    """Not found error."""
    
    status_code = 404
    default_detail = 'Resource not found'


class PermissionError(ClassHubException):
    """Permission error."""
    
    status_code = 403
    default_detail = 'Permission denied'


class AuthenticationError(ClassHubException):
    """Authentication error."""
    
    status_code = 401
    default_detail = 'Authentication required'


class RateLimitError(ClassHubException):
    """Rate limit error."""
    
    status_code = 429
    default_detail = 'Too many requests'


class ConflictError(ClassHubException):
    """Conflict error."""
    
    status_code = 409
    default_detail = 'Resource conflict'


class ServiceUnavailableError(ClassHubException):
    """Service unavailable error."""
    
    status_code = 503
    default_detail = 'Service unavailable'
