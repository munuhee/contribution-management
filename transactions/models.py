import random
import string
from django.db import models
from cases.models import Case


class Invoice(models.Model):
    member = models.ForeignKey(
        'members.Member',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    invoice_number = models.CharField(
        max_length=100,
        unique=True
    )
    issue_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    outstanding_balance = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    is_settled = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk and self.outstanding_balance is None:
            self.outstanding_balance = self.amount
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.amount}"


class Transaction(models.Model):
    COMMENT_CHOICES = [
        ('INVOICE_CREATION', 'Invoice Creation'),
        ('INVOICE_PAYMENT', 'Invoice Payment'),
        ('INV_PARTIAL_PAY', 'Inv Partial Pay'),
        ('PENALTY_PAYMENT', 'Penalty Payment'),
        ('ACCOUNT_TOPUP', 'Account Top-up'),
    ]
    member = models.ForeignKey(
        'members.Member', on_delete=models.CASCADE, blank=True, null=True
    )
    trans_id = models.CharField(max_length=20, blank=True)
    reference = models.CharField(max_length=20, unique=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    invoice = models.ForeignKey(
        Invoice, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='transactions'
    )
    comment = models.CharField(
        max_length=20, choices=COMMENT_CHOICES, default='ACCOUNT_TOPUP'
    )

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = self.generate_reference()
        super().save(*args, **kwargs)

    def generate_reference(self):
        random_suffix = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=6
        ))
        return f"MSBK{random_suffix}"

    def __str__(self):
        return f"{self.reference} - {self.amount}"


class UnmatchedTransaction(models.Model):
    trans_id = models.CharField(max_length=20, blank=True)
    reference = models.CharField(max_length=20, unique=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    is_settled = models.BooleanField(default=False)
    comment = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = self.generate_reference()
        super(UnmatchedTransaction, self).save(*args, **kwargs)

    def generate_reference(self):
        random_suffix = ''.join(
            random.choices(string.ascii_uppercase + string.digits, k=6)
        )
        return f"UT{random_suffix}"

    def __str__(self):
        return f"{self.reference} - {self.amount}"
