from django import forms
from .models import Member


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = [
            'first_name', 'last_name', 'phone_number',
            'member_number', 'national_id_number', 'account_balance'
        ]
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter first name'
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter last name'
                }
            ),
            'phone_number': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter phone number'
                }
            ),
            'member_number': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter member number'
                }
            ),
            'national_id_number': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter national ID number'
                }
            ),
            'account_balance': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'step': '0.01',
                    'placeholder': 'Enter account balance'
                }
            ),
        }
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'phone_number': 'Phone Number',
            'member_number': 'Member Number',
            'national_id_number': 'National ID Number',
            'account_balance': 'Account Balance (KES)',
        }
