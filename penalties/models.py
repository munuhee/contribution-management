from django.db import models
from django.apps import apps
from cases.models import Case


class Penalty(models.Model):
    # Declare ForeignKey with a placeholder for now
    member = models.ForeignKey('members.Member', on_delete=models.CASCADE)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Perform the model lookup
        if isinstance(self.member, str):
            self.member = apps.get_model(
                'members', 'Member'
            ).objects.get(id=self.member)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Penalty for {self.member} on {self.case}"
