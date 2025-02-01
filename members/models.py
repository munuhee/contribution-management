from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from penalties.models import Penalty

# Validator to ensure phone numbers include a country code.
phone_regex = RegexValidator(
    regex=r'^\+\d{10,15}$',
    message=(
        "Phone number must be in the format: "
        "+254712345678' and contain only digits after the '+'."
    )
)


class Member(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, validators=[phone_regex])
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
