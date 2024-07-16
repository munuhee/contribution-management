from django.db import models
from django.utils import timezone
from datetime import timedelta


class Case(models.Model):
    case_number = models.CharField(max_length=10, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.deadline = timezone.now() + timedelta(days=7)
        super(Case, self).save(*args, **kwargs)

    def __str__(self):
        return self.case_number
