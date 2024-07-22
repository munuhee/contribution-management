from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Transaction
from .forms import TransactionForm


# List all transactions
@login_required
def list_transactions(request):
    transactions = Transaction.objects.all()
    return render(
        request,
        'transactions/transactions_list.html',
        {'transactions': transactions}
    )


# Add a new transaction
@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_transactions')
    else:
        form = TransactionForm()
    return render(
        request, 'transactions/transactions_form.html', {'form': form}
    )


# Update a transaction
@login_required
def update_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('list_transactions')
    else:
        form = TransactionForm(instance=transaction)
    return render(
        request, 'transactions/transactions_form.html', {'form': form}
    )


# Delete a transaction
@login_required
def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    transaction.delete()
    return redirect('list_transactions')
