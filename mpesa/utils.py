"""
This module provides functionality for interacting with the MPESA API, specifically
for obtaining an access token and registering URLs for payment notifications and validation.

It includes two main functions:

1. `get_access_token()`: Retrieves an access token from the MPESA API using the consumer key and secret.
2. `register_urls()`: Registers the ShortCode, response type, and confirmation/validation URLs with MPESA.

The module uses the `requests` library for HTTP requests and the `base64` module for encoding
the API key to perform Basic Authentication. Configuration settings (e.g., consumer key, secret,
URLs) are defined in Django settings.
"""

import json
import base64
import requests
from django.conf import settings


def get_access_token():
    try:
        api_key = (
            f"{settings.MPESA_CONSUMER_KEY}:{settings.MPESA_CONSUMER_SECRET}"
        )
        encoded_key = base64.b64encode(api_key.encode()).decode()

        headers = {
            'Authorization': f'Basic {encoded_key}',
            'Content-Type': 'application/json'
        }

        response = requests.get(settings.MPESA_AUTH_URL, headers=headers)
        response.raise_for_status()
        return response.json().get('access_token')
    except requests.RequestException as e:
        print(f"Error obtaining access token: {e}")
        return None


def register_urls():
    access_token = get_access_token()
    if not access_token:
        print("Failed to obtain access token")
        return

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    payload = {
        "ShortCode": settings.MPESA_SHORTCODE,
        "ResponseType": "Completed",
        "ConfirmationURL": settings.CONFIRMATION_URL,
        "ValidationURL": settings.VALIDATION_URL,
    }

    response = requests.post(
        settings.MPESA_REGISTER_URL,
        headers=headers,
        data=json.dumps(payload)
    )
    print(response.text.encode('utf8'))
