from django.db import models
from members.models import Member
from cases.models import Case


class Penalty(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Penalty for {self.member} on {self.case}"
