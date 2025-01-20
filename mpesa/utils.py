"""
This module provides functionality for interacting with the MPESA API,
specifically for obtaining an access token and
registering URLs for payment notifications and validation.

It includes two main functions:

1. `get_access_token()`: Retrieves an access token from the MPESA API.
2. `register_urls()`:  Register the callback URLs
to your pay bill.

The module uses the `requests` library for HTTP requests
and the `base64` module for encoding the API key to
perform Basic Authentication.

Configuration settings (e.g., consumer key, secret,
URLs) are defined in Django settings.
"""

import json
import base64
import requests
import logging
from django.conf import settings

# logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def get_access_token():
    """
    Retrieves an access token from the MPESA API.
    """
    try:
        logger.info("Attempting to obtain access token.")
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

        access_token = response.json().get('access_token')
        if access_token:
            logger.info("Access token obtained successfully.")
            return access_token
        else:
            logger.error("Failed to retrieve access token from the response.")
            return None
    except requests.RequestException as e:
        logger.error(f"Error obtaining access token: {e}")
        return None


def register_urls():
    """
    Registers callback URLs.
    """
    logger.info("Starting URL registration process.")
    access_token = get_access_token()
    if not access_token:
        logger.error(
            "Failed to obtain access token. URL registration aborted."
        )
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

    try:
        logger.info("Sending URL registration request.")
        response = requests.post(
            settings.MPESA_REGISTER_URL,
            headers=headers,
            data=json.dumps(payload)
        )
        response.raise_for_status()
        logger.info(f"URL registration successful: {response.text}")
    except requests.RequestException as e:
        logger.error(f"Error during URL registration: {e}")
