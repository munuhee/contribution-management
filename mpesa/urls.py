from django.urls import path
from .views import MpesaValidationView, MpesaConfirmationView

urlpatterns = [
    path(
        'validation/',
        MpesaValidationView.as_view(),
        name='mpesa_validation'
    ),
    path(
        'confirmation/',
        MpesaConfirmationView.as_view(),
        name='mpesa_confirmation'
    ),
]
