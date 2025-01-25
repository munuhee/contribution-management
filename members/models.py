from django.db import models
from django.conf import settings
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

    def apply_penalty(self, invoice):
        penalty_amount = settings.PENALTY_AMOUNT
        Penalty.objects.create(
            member=self,
            invoice=invoice,
            amount=penalty_amount,
            is_paid=False
        )
