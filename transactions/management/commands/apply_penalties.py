from django.core.management.base import BaseCommand
from django.utils import timezone
from transactions.models import Invoice


class Command(BaseCommand):
    help = 'Apply penalties for overdue invoices'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        overdue_invoices = Invoice.objects.filter(
            due_date__lt=now,
            is_settled=False
        )

        for invoice in overdue_invoices:
            member = invoice.member
            if member:
                member.apply_penalty(invoice)
                self.stdout.write(self.style.SUCCESS(
                    f'Applied penalty for member {member} '
                    f'on invoice {invoice.invoice_number}'
                ))
            else:
                self.stdout.write(self.style.WARNING(
                    f'No member associated with '
                    f'invoice {invoice.invoice_number}'
                ))
