from django import forms
from .models import Member


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = [
            'first_name', 'last_name', 'phone_number',
            'member_number', 'national_id', 'account_balance'
        ]
