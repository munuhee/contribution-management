import logging
from django.http import JsonResponse

logger = logging.getLogger(__name__)


def handle_exceptions(view_func):
    def wrapper(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return JsonResponse(
                {"status": "error", "message": "Internal server error"},
                status=500,
            )
    return wrapper
