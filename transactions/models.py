import random
import string
from django.db import models
from members.models import Member


class Transaction(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    trans_id = models.CharField(max_length=20, unique=True, blank=True)
    reference = models.CharField(max_length=20, unique=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = self.generate_reference()
        super(Transaction, self).save(*args, **kwargs)

    def generate_reference(self):
        random_suffix = ''.join(
            random.choices(string.ascii_uppercase + string.digits, k=6)
        )
        return f"MSBK{random_suffix}"

    def __str__(self):
        return f"{self.reference} - {self.amount}"


class UnmatchedTransactions(models.Model):
    trans_id = models.CharField(max_length=20, blank=True)
    reference = models.CharField(max_length=20, unique=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = self.generate_reference()
        super(Transaction, self).save(*args, **kwargs)

    def generate_reference(self):
        random_suffix = ''.join(
            random.choices(string.ascii_uppercase + string.digits, k=6)
        )
        return f"UT{random_suffix}"

    def __str__(self):
        return f"{self.reference} - {self.amount}"
