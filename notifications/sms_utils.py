import requests
from django.conf import settings


def send_sms(to, message):
    url = 'https://api.sandbox.africastalking.com/version1/messaging'

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'apiKey': settings.AFRICA_TALKING_API_KEY,
    }

    data = {
        'username': settings.AFRICA_TALKING_USERNAME,
        'to': to,
        'message': message,
        'from': 'Msingi Bora/Kirathimo',  # Optional
    }

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        return response.json()
    else:
        # Log the error or raise an exception as needed
        return None
