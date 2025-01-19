from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Transaction
from .forms import TransactionForm


# List all transactions
@login_required
def list_transactions(request):
    query = request.GET.get('search', '').strip()
    if query:
        # Filter transactions based on the query
        transactions = Transaction.objects.filter(
            Q(member__member_number__icontains=query) |
            Q(trans_id__icontains=query) |
            Q(reference__icontains=query) |
            Q(phone_number__icontains=query)
        )
    else:
        transactions = Transaction.objects.all()

    # Implement pagination
    paginator = Paginator(transactions, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'transactions/transactions_list.html',
        {'page_obj': page_obj, 'search_query': query}
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
