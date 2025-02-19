from django import forms
from .models import Transaction, UnmatchedTransaction, Invoice


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['member', 'amount', 'invoice', 'comment']
        widgets = {
            'amount': forms.NumberInput(
                attrs={
                    'class': 'bg-gray-50 border border-gray-300 text-gray-900'
                    'text-sm rounded-lg focus:ring-blue-500 '
                    'focus:border-blue-500'
                    'block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600'
                    'dark:placeholder-gray-400 dark:text-white'
                    ' dark:focus:ring-blue-500 dark:focus:border-blue-500',
                    'step': '0.01'
                    }
                ),
            'member': forms.Select(
                attrs={
                    'class': 'bg-gray-50 border border-gray-300 text-gray-900'
                    'text-sm rounded-lg focus:ring-blue-500'
                    'focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700'
                    'dark:border-gray-600 dark:placeholder-gray-400'
                    'dark:text-white dark:focus:ring-blue-500'
                    'dark:focus:border-blue-500'
                    }
                ),
            'comment': forms.Select(
                attrs={
                    'class': 'bg-gray-50 border border-gray-300 text-gray-900'
                    'text-sm rounded-lg focus:ring-blue-500'
                    'focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700'
                    'dark:border-gray-600 dark:placeholder-gray-400'
                    'dark:text-white dark:focus:ring-blue-500'
                    'dark:focus:border-blue-500'
                }
            )
        }

        labels = {
            'member': 'Member',
            'amount': 'Amount (KES)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the 'INVOICE_CREATION' option from the comment choices
        self.fields['comment'].choices = [
            choice for choice in self.fields['comment'].choices
            if choice[0] != 'INVOICE_CREATION'
        ]

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError('Amount must be greater than zero.')
        return amount


class UnmatchedTransactionForm(forms.ModelForm):
    class Meta:
        model = UnmatchedTransaction
        fields = [
            'trans_id', 'reference', 'phone_number',
            'amount', 'is_settled', 'comment'
        ]
        widgets = {
            'trans_id': forms.TextInput(
                attrs={
                    'class': 'bg-gray-50 border border-gray-300 text-gray-900'
                    'text-sm rounded-lg focus:ring-blue-500'
                    'focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700'
                    'dark:border-gray-600 dark:placeholder-gray-400'
                    'dark:text-white dark:focus:ring-blue-500'
                    'dark:focus:border-blue-500',
                    'step': '0.01'
                    }
                ),
            'reference': forms.TextInput(
                attrs={
                    'class': 'bg-gray-50 border border-gray-300 text-gray-900'
                    'text-sm rounded-lg focus:ring-blue-500'
                    'focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700'
                    'dark:border-gray-600 dark:placeholder-gray-400'
                    'dark:text-white dark:focus:ring-blue-500'
                    'dark:focus:border-blue-500',
                    'step': '0.01'
                    }
                ),
            'phone_number': forms.TextInput(
                attrs={
                    'class': 'bg-gray-50 border border-gray-300 text-gray-900'
                    'text-sm rounded-lg focus:ring-blue-500'
                    'focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700'
                    'dark:border-gray-600 dark:placeholder-gray-400'
                    'dark:text-white dark:focus:ring-blue-500'
                    'dark:focus:border-blue-500',
                    'step': '0.01'
                    }
                ),
            'amount': forms.NumberInput(
                attrs={
                    'class': 'bg-gray-50 border border-gray-300 text-gray-900'
                    'text-sm rounded-lg focus:ring-blue-500'
                    'focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700'
                    'dark:border-gray-600 dark:placeholder-gray-400'
                    'dark:text-white dark:focus:ring-blue-500'
                    'dark:focus:border-blue-500',
                    'step': '0.01'
                    }
                ),
            'is_settled': forms.CheckboxInput(
                attrs={
                    'class': 'bg-gray-50 border border-gray-300 text-gray-900'
                    'text-sm rounded-lg focus:ring-blue-500'
                    'focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700'
                    'dark:border-gray-600 dark:placeholder-gray-400'
                    'dark:text-white dark:focus:ring-blue-500'
                    'dark:focus:border-blue-500',
                    }
            ),
            'comment': forms.Textarea(
                attrs={
                    'class': 'bg-gray-50 border border-gray-300 text-gray-900'
                    'text-sm rounded-lg focus:ring-blue-500'
                    'focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700'
                    'dark:border-gray-600 dark:placeholder-gray-400'
                    'dark:text-white dark:focus:ring-blue-500'
                    'dark:focus:border-blue-500',
                    'rows': 2,
                }
            )
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


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            'member', 'case', 'due_date',
            'amount', 'description', 'is_settled'
        ]
        widgets = {
            'member': forms.Select(
                attrs={
                    'class': 'bg-gray-50 border border-gray-300 text-gray-900'
                    'text-sm rounded-lg focus:ring-blue-500'
                    'focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700'
                    'dark:border-gray-600 dark:placeholder-gray-400'
                    'dark:text-white dark:focus:ring-blue-500'
                    'dark:focus:border-blue-500',
                    'step': '0.01'
                }
            ),
            'case': forms.Select(
                attrs={
                    'class': 'bg-gray-50 border border-gray-300 text-gray-900'
                    'text-sm rounded-lg focus:ring-blue-500'
                    'focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700'
                    'dark:border-gray-600 dark:placeholder-gray-400'
                    'dark:text-white dark:focus:ring-blue-500'
                    'dark:focus:border-blue-500',
                    'step': '0.01'
                }
            ),
            'due_date': forms.DateTimeInput(
                attrs={
                    'class': 'bg-gray-50 border border-gray-300 text-gray-900'
                    'text-sm rounded-lg focus:ring-blue-500'
                    'focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700'
                    'dark:border-gray-600 dark:placeholder-gray-400'
                    'dark:text-white dark:focus:ring-blue-500'
                    'dark:focus:border-blue-500',
                    'type': 'datetime-local'
                }
            ),
            'amount': forms.NumberInput(
                attrs={
                    'class': 'bg-gray-50 border border-gray-300 text-gray-900'
                    'text-sm rounded-lg focus:ring-blue-500'
                    'focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700'
                    'dark:border-gray-600 dark:placeholder-gray-400'
                    'dark:text-white dark:focus:ring-blue-500'
                    'dark:focus:border-blue-500'
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'bg-gray-50 border border-gray-300 text-gray-900'
                    'text-sm rounded-lg focus:ring-blue-500'
                    'focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700'
                    'dark:border-gray-600 dark:placeholder-gray-400'
                    'dark:text-white dark:focus:ring-blue-500'
                    'dark:focus:border-blue-500',
                    'rows': 2,
                    'step': '0.01'
                }
            ),
            'is_settled': forms.CheckboxInput(
                attrs={
                    'class': 'bg-gray-50 border border-gray-300 text-gray-900'
                    'text-sm rounded-lg focus:ring-blue-500'
                    'focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700'
                    'dark:border-gray-600 dark:placeholder-gray-400'
                    'dark:text-white dark:focus:ring-blue-500'
                    'dark:focus:border-blue-500',
                    'step': '0.01'
                }
            )
        }
