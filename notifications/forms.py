from django import forms


class SendBulkSMSForm(forms.Form):
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Enter your message here...'
        }),
        help_text="Enter the message to send to all members.",
        label="Message"
    )
