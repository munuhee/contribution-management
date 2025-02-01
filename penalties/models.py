from django.db import models
from django.apps import apps
from transactions.models import Invoice


class Penalty(models.Model):
    member = models.ForeignKey('members.Member', on_delete=models.CASCADE)
    invoice = models.ForeignKey(
        Invoice, on_delete=models.CASCADE,
        blank=True, null=True
    )
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    comment = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        # Perform the model lookup
        if isinstance(self.member, str):
            self.member = apps.get_model(
                'members', 'Member'
            ).objects.get(id=self.member)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Penalty for {self.member} on {self.invoice}"
