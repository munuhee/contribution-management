from django.core.management.base import BaseCommand
from mpesa.utils import register_urls


class Command(BaseCommand):
    help = 'Register M-Pesa URLs'

    def handle(self, *args, **kwargs):
        register_urls()
