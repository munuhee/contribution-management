from django.urls import path
from .views import list_transactions, add_transaction, update_transaction, delete_transaction

urlpatterns = [
    path('', list_transactions, name='list_transactions'),
    path('add/', add_transaction, name='add_transaction'),
    path(
        'update/<int:transaction_id>/',
        update_transaction, name='update_transaction'
    ),
    path(
        'delete/<int:transaction_id>/',
        delete_transaction,
        name='delete_transaction'
    ),
]
