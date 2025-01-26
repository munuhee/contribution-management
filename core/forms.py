from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordResetForm
from django.urls import reverse
from django.core.mail import send_mail


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'bg-gray-50 border border-gray-300 text-gray-900'
        'text-sm rounded-lg focus:ring-blue-500'
        'focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700'
        'dark:border-gray-600 dark:placeholder-gray-400'
        'dark:text-white dark:focus:ring-blue-500'
        'dark:focus:border-blue-500',
        'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'bg-gray-50 border border-gray-300 text-gray-900'
        'text-sm rounded-lg focus:ring-blue-500'
        'focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700'
        'dark:border-gray-600 dark:placeholder-gray-400'
        'dark:text-white dark:focus:ring-blue-500'
        'dark:focus:border-blue-500',
        'placeholder': 'Password'
    }))


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full p-3 text-sm border rounded-lg'
            'focus:outline-none focus:ring-2 focus:ring-blue-500'
            'focus:border-blue-500 placeholder-gray-400'
            'dark:bg-gray-800 dark:text-white dark:placeholder-gray-500'
            'dark:border-gray-700',
            'placeholder': 'Enter your email address'
        })
    )

    def save(self, *args, **kwargs):
        email = self.cleaned_data["email"]
        subject = "Password Reset Request"
        message = (
            "You have requested to reset your password.\n\n"
            "Please click the link below to set a new password:\n\n"
            f"{reverse('password_reset_confirm', kwargs={
                'uidb64': 'uid_value', 'token': 'token_value'
                })}\n\n"
            "If you did not make this request, please ignore this email."
        )

        send_mail(
            subject,
            message,
            'from@example.com',
            [email]
        )
