from django import forms
from .models import Penalty


class PenaltyForm(forms.ModelForm):
    class Meta:
        model = Penalty
        fields = ['member', 'invoice', 'amount', 'is_paid', 'comment']
        widgets = {
            'member': forms.Select(
                attrs={
                    'class': 'bg-gray-50 border border-gray-300'
                    'text-gray-900 text-sm rounded-lg focus:ring-blue-500'
                    'focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700'
                    'dark:border-gray-600 dark:placeholder-gray-400'
                    'dark:text-white dark:focus:ring-blue-500'
                    'dark:focus:border-blue-500',
                    'aria-label': 'Select Member'
                }
            ),
            'invoice': forms.Select(
                attrs={
                    'class': 'bg-gray-50 border border-gray-300'
                    'text-gray-900 text-sm rounded-lg focus:ring-blue-500'
                    'focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700'
                    'dark:border-gray-600 dark:placeholder-gray-400'
                    'dark:text-white dark:focus:ring-blue-500'
                    'dark:focus:border-blue-500',
                    'aria-label': 'Select invoice'
                }
            ),
            'amount': forms.NumberInput(
                attrs={
                    'class': 'bg-gray-50 border border-gray-300'
                    'text-gray-900 text-sm rounded-lg focus:ring-blue-500'
                    'focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700'
                    'dark:border-gray-600 dark:placeholder-gray-400'
                    'dark:text-white dark:focus:ring-blue-500'
                    'dark:focus:border-blue-500',
                    'step': '0.01',
                    'placeholder': 'Enter amount'
                }
            ),
            'is_paid': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                    'aria-label': 'Is Paid'
                }
            ),
            'comment': forms.Textarea(
                attrs={
                    'class': 'bg-gray-50 border border-gray-300'
                    'text-gray-900 text-sm rounded-lg focus:ring-blue-500'
                    'focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700'
                    'dark:border-gray-600 dark:placeholder-gray-400'
                    'dark:text-white dark:focus:ring-blue-500'
                    'dark:focus:border-blue-500',
                    'rows': '2',
                    'step': '0.01',
                    'placeholder': 'Enter a comment'
                }
            )
        }
        labels = {
            'member': 'Member',
            'invoice': 'Invoice',
            'amount': 'Penalty Amount',
            'comment': 'comment',
            'is_paid': 'Payment Status',
        }
        help_texts = {
            'amount': 'Enter the penalty amount in the specified currency.',
            'is_paid': 'Check this box if the penalty has been paid.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set a custom empty label for the invoice field
        self.fields['invoice'].empty_label = "Not Applicable"

        for field in self.fields.values():
            field.error_messages = {'required': f'{field.label} is required.'}
