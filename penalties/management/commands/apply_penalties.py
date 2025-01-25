from django.core.management.base import BaseCommand
import logging
from penalties.utils import apply_penalties

# Get the logger
logger = logging.getLogger('penalties')


class Command(BaseCommand):
    help = 'Apply penalties to overdue invoices'

    def handle(self, *args, **kwargs):
        logger.info("Starting penalty application process.")
        apply_penalties()
        logger.info("Penalty application process completed.")
        self.stdout.write(
            self.style.SUCCESS("Penalties applied to overdue invoices.")
        )
