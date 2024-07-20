from django.urls import path
from .views import send_bulk_sms, list_sent_messages

urlpatterns = [
    path('send_bulk_sms/', send_bulk_sms, name='send_bulk_sms'),
    path('sent_messages/', list_sent_messages, name='list_sent_messages'),
]
