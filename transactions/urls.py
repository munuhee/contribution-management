from django.urls import path
from . import views  # Import views module

urlpatterns = [
    path('', views.list_transactions, name='list_transactions'),
    path('add/', views.add_transaction, name='add_transaction'),
    path(
        'update/<int:transaction_id>/',
        views.update_transaction, name='update_transaction'
    ),
    path(
        'delete/<int:transaction_id>/',
        views.delete_transaction,
        name='delete_transaction'
    ),
    path(
        'unmatched/', views.unmatched_transactions_list,
        name='unmatched_transactions_list'
    ),
    path(
        'unmatched/add/', views.add_unmatched_transaction,
        name='add_unmatched_transaction'
    ),
    path(
        'unmatched/<int:pk>/update/', views.update_unmatched_transaction,
        name='update_unmatched_transaction'
    ),
    path(
        'unmatched/<int:pk>/delete/', views.delete_unmatched_transaction,
        name='delete_unmatched_transaction'
    ),
    path(
        'transactions/export-pdf/', views.export_transactions_pdf,
        name='export_transactions_pdf'
    ),
    path(
        'invoices/',
        views.invoice_list, name='invoice_list'
    ),
    path(
        'invoices/<int:pk>/',
        views.invoice_detail, name='invoice_detail'
    ),
    path(
        'invoices/create/',
        views.invoice_create, name='invoice_create'
    ),
    path(
        'invoices/<int:pk>/update/',
        views.invoice_update, name='invoice_update'
    ),
    path(
        'invoices/<int:pk>/delete/',
        views.invoice_delete, name='invoice_delete'
    ),
]
