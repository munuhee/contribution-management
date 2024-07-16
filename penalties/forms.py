from django import forms
from .models import Penalty


class PenaltyForm(forms.ModelForm):
    class Meta:
        model = Penalty
        fields = ['member', 'case', 'amount', 'is_paid']
        widgets = {
            'member': forms.Select(
                attrs={'class': 'form-control', 'aria-label': 'Select Member'}
            ),
            'case': forms.Select(
                attrs={'class': 'form-control', 'aria-label': 'Select Case'}
            ),
            'amount': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': 'Enter amount'}
            ),
            'is_paid': forms.CheckboxInput(
                attrs={'class': 'form-check-input', 'aria-label': 'Is Paid'}
            ),
        }
        labels = {
            'member': 'Member',
            'case': 'Case',
            'amount': 'Penalty Amount',
            'is_paid': 'Payment Status',
        }
        help_texts = {
            'amount': 'Enter the penalty amount in the specified currency.',
            'is_paid': 'Check this box if the penalty has been paid.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.error_messages = {'required': f'{field.label} is required.'}
