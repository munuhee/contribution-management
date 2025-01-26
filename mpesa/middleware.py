import logging
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

# Configure logging
logger = logging.getLogger(__name__)


class IPWhitelistMiddleware(MiddlewareMixin):
    WHITELISTED_IPS = [
        "196.201.214.200", "196.201.214.206", "196.201.213.114",
        "196.201.214.207", "196.201.214.208", "196.201.213.44",
        "196.201.212.127", "196.201.212.138", "196.201.212.129",
        "196.201.212.136", "196.201.212.74", "196.201.212.69",
    ]

    def process_request(self, request):
        client_ip = request.META.get('REMOTE_ADDR')
        if client_ip not in self.WHITELISTED_IPS:
            # Log unauthorized access attempt
            logger.warning(f"Unauthorized access attempt from IP: {client_ip}")
            return JsonResponse(
                {"error": "Unauthorized IP address."}, status=403
            )

        # Log successful access
        logger.info(f"Access granted for IP: {client_ip}")
