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
    path('unmatched/', views.unmatched_transactions_list, name='unmatched_transactions_list'),
    path('unmatched/add/', views.add_unmatched_transaction, name='add_unmatched_transaction'),
    path('unmatched/<int:pk>/update/', views.update_unmatched_transaction, name='update_unmatched_transaction'),
    path('unmatched/<int:pk>/delete/', views.delete_unmatched_transaction, name='delete_unmatched_transaction'),
]
