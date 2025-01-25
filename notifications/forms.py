from django import forms


class SendBulkSMSForm(forms.Form):
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'bg-gray-50 border border-gray-300'
            'text-gray-900 text-sm rounded-lg focus:ring-blue-500'
            'focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700'
            'dark:border-gray-600 dark:placeholder-gray-400 dark:text-white'
            'dark:focus:ring-blue-500 dark:focus:border-blue-500',
            'rows': 5,
            'placeholder': 'Enter your message here...'
        }),
        help_text="Enter the message to send to all members.",
        label="Message"
    )
