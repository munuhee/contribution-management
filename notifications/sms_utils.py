"""
Sends an SMS using the Africa's Talking SDK.

This module provides utility functions for sending SMS messages using the Africa's Talking SDK.

Dependencies:
    - `africastalking`: The Africa's Talking Python SDK.
    - Django settings:
        - `AFRICA_TALKING_API_KEY`: The API key for authenticating requests.
        - `AFRICA_TALKING_USERNAME`: The Africa's Talking account username.
"""

import africastalking
import logging
from django.conf import settings

# Set up logging
logger = logging.getLogger(__name__)

# Initialize Africa's Talking SDK
africastalking.initialize(
    settings.AFRICA_TALKING_USERNAME,
    settings.AFRICA_TALKING_API_KEY
)
sms = africastalking.SMS


def send_sms(to, message):
    """
    Sends an SMS message to a single recipient using Africa's Talking.

    Args:
        to (str): The recipient's phone number (e.g., "+254712345678").
        message (str): The text message to be sent.

    Returns:
        dict: The response from Africa's Talking API.
    """
    try:
        logger.info(f"Sending SMS to {to} with message: {message}")
        response = sms.send(message, [to])
        logger.info(f"SMS sent successfully to {to}: {response}")
        return response
    except Exception as e:
        logger.error(f"Error sending SMS to {to}: {str(e)}")
        return {"error": str(e)}
