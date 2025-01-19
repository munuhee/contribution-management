"""
Sends an SMS using the Africa's Talking API.

This function allows sending SMS messages to a specified recipient using the Africa's Talking messaging API.
The API credentials and other settings are configured in Django settings.

Args:
    to (str): The recipient's phone number in international format (e.g., +254712345678).
    message (str): The text message to be sent.

Returns:
    dict: The response from the Africa's Talking API if the request is successful.
    None: If the API request fails (e.g., non-200 status code).

Dependencies:
    - `requests`: For making HTTP POST requests.
    - Django settings:
        - `AFRICA_TALKING_API_KEY`: The API key for authenticating requests.
        - `AFRICA_TALKING_USERNAME`: The Africa's Talking account username.
"""

import requests
from django.conf import settings


def send_sms(to, message):
    url = settings.AFRICA_TALKING_API_URL
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'apiKey': settings.AFRICA_TALKING_API_KEY,
    }

    data = {
        'username': settings.AFRICA_TALKING_USERNAME,
        'to': to,
        'message': message,
        'from': 'Msingi Bora/Kirathimo',
    }

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        return response.json()
    else:
        return None
