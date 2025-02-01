from django import forms
from .models import Case


class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ['case_number', 'amount', 'description', 'deadline']
        widgets = {
            'case_number': forms.TextInput(attrs={
                'class': 'bg-gray-50 border border-gray-300 text-gray-900'
                'text-sm rounded-lg focus:ring-blue-500'
                'focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700'
                'dark:border-gray-600 dark:placeholder-gray-400'
                'dark:text-white dark:focus:ring-blue-500'
                'dark:focus:border-blue-500',
                'placeholder': 'Enter case number'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'bg-gray-50 border border-gray-300 text-gray-900'
                'text-sm rounded-lg focus:ring-blue-500'
                'focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700'
                'dark:border-gray-600 dark:placeholder-gray-400'
                'dark:text-white dark:focus:ring-blue-500'
                'dark:focus:border-blue-500',
                'step': '0.01', 'placeholder': 'Enter amount'
            }),
            'description': forms.Textarea(attrs={
                'class': 'bg-gray-50 border border-gray-300 text-gray-900'
                'text-sm rounded-lg focus:ring-blue-500'
                'focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700'
                'dark:border-gray-600 dark:placeholder-gray-400'
                'dark:text-white dark:focus:ring-blue-500'
                'dark:focus:border-blue-500',
                'rows': 2, 'placeholder': 'Enter description'
            }),
            'deadline': forms.DateTimeInput(attrs={
                'class': 'bg-gray-50 border border-gray-300 text-gray-900'
                'text-sm rounded-lg focus:ring-blue-500'
                'focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700'
                'dark:border-gray-600 dark:placeholder-gray-400'
                'dark:text-white dark:focus:ring-blue-500'
                'dark:focus:border-blue-500',
                'type': 'datetime-local'
            }),
        }
        labels = {
            'case_number': 'Case Number', 'amount': 'Amount (KES)',
            'description': 'Description', 'deadline': 'Deadline'
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
