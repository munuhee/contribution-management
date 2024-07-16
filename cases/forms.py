from django import forms
from .models import Case


class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ['case_number', 'amount', 'description', 'deadline']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        labels = {
            'case_number': 'Case Number',
            'amount': 'Amount (KES)',
            'description': 'Description',
            'deadline': 'Deadline',
        }

    def clean_case_number(self):
        case_number = self.cleaned_data.get('case_number')
        if not case_number:
            raise forms.ValidationError('Case number is required.')
        return case_number

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError('Amount must be greater than zero.')
        return amount
