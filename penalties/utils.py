import uuid
import logging
from django.conf import settings
from django.utils.timezone import now
from transactions.models import Invoice, Transaction
from .models import Penalty

# Get the logger
logger = logging.getLogger('penalties')


# Corrected apply_penalties function in utils.py
def apply_penalties():
    overdue_invoices = Invoice.objects.filter(
        due_date__lt=now(),
        is_settled=False
    )

    for invoice in overdue_invoices:
        if invoice.member is None:
            logger.error(
                f"Invoice {invoice.invoice_number} has no associated member."
            )
            continue

        penalty_exists = Penalty.objects.filter(invoice=invoice).exists()

        if not penalty_exists:
            Penalty.objects.create(
                member=invoice.member,
                invoice=invoice,
                amount=getattr(settings, 'PENALTY_AMOUNT', 100),
                is_paid=False
            )

            Transaction.objects.create(
                member=invoice.member,
                amount=getattr(settings, 'PENALTY_AMOUNT', 100),
                comment='PENALTY_CREATION',
                trans_id=f"TXN{uuid.uuid4().hex[:6].upper()}",
                reference=f"MSBK{uuid.uuid4().hex[:6].upper()}",
            )
