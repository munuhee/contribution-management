from django import forms
from .models import Transaction


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['member', 'amount']
        widgets = {
            'amount': forms.NumberInput(attrs={'step': '0.01'}),
        }
        labels = {
            'member': 'Member',
            'amount': 'Amount (KES)',
        }

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError('Amount must be greater than zero.')
        return amount
