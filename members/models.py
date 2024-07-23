from django.db import models
from transactions.models import Transaction
from penalties.models import Penalty


class Member(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    member_number = models.CharField(max_length=10, unique=True)
    national_id_number = models.CharField(max_length=20)
    account_balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def settle_invoice(self, invoice):
        self.account_balance -= invoice.amount
        self.save()
        Transaction.objects.create(
            member=self,
            transaction_type="Invoice",
            amount=invoice.amount,
            trans_id=invoice.invoice_number,
            invoice=invoice
        )

        if self.account_balance >= invoice.amount:
            Transaction.objects.create(
                member=self,
                transaction_type="Invoice Payment",
                amount=invoice.amount,
                trans_id=invoice.invoice_number
            )

            invoice.is_settled = True
            invoice.save()
            return True
        else:
            return False

    def apply_penalty(self, invoice):
        penalty_amount = invoice.amount * 0.10
        self.account_balance -= penalty_amount
        self.save()

        Penalty.objects.create(
            member=self,
            case=invoice.case,
            amount=penalty_amount
        )
