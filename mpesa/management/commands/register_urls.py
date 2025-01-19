"""
Django management command to register M-Pesa URLs.

This module defines a custom Django management command that, when executed,
will trigger the registration of M-Pesa URLs used for payment notifications
and validation. The command calls the `register_urls()` function from the
`mpesa.utils` module to handle the registration process.

Usage:
    python manage.py register_mpesa_urls
"""

from django.core.management.base import BaseCommand
from mpesa.utils import register_urls


class Command(BaseCommand):
    help = 'Register M-Pesa URLs'

    def handle(self, *args, **kwargs):
        register_urls()
