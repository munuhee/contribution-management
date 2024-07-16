from django.urls import path
from .views import MpesaCallbackView

urlpatterns = [
    path(
        'mpesa-callback/', MpesaCallbackView.as_view(), name='mpesa_callback'
    ),
]
