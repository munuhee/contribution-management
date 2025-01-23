from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.template.loader import render_to_string
from .models import Transaction, UnmatchedTransaction, Invoice
from .forms import TransactionForm, UnmatchedTransactionForm
import uuid


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

    # Ensure consistent ordering
    transactions = transactions.order_by('-date')

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
            transaction = form.save(commit=False)
            transaction.trans_id = f"TXN-{uuid.uuid4().hex[:4].upper()}"
            transaction.reference = f"REF-{uuid.uuid4().hex[:4].upper()}"

            # Handling based on the transaction comment type
            if transaction.comment == 'INVOICE_PAYMENT' and transaction.member:
                member = transaction.member
                outstanding_invoices = Invoice.objects.filter(
                    member=member, is_settled=False
                ).order_by('issue_date')

                amount_remaining = transaction.amount
                for invoice in outstanding_invoices:
                    if amount_remaining <= 0:
                        break

                    if invoice.amount <= amount_remaining:
                        # Fully settle the invoice
                        amount_remaining -= invoice.amount
                        invoice.is_settled = True
                        invoice.save()

                        # Create a transaction for the invoice
                        invoice_transaction = Transaction(
                            member=member,
                            amount=invoice.amount,
                            comment='INVOICE_PAYMENT',
                            trans_id=invoice.invoice_number,
                            reference=f"REF-{uuid.uuid4().hex[:4].upper()}",
                            phone_number="-",
                            invoice=invoice,
                        )
                        invoice_transaction.save()
                        member.account_balance += invoice.amount
                        member.save()
                    else:
                        # Partially settle the invoice
                        invoice.amount -= amount_remaining
                        amount_remaining = 0
                        invoice.save()

                # Add any remaining amount as a top-up
                if amount_remaining > 0:
                    # Add remaining amount to the member's balance
                    member.account_balance += amount_remaining
                    member.save()

                    # Create a top-up transaction for the remaining amount
                    top_up_transaction = Transaction(
                        member=member,
                        amount=amount_remaining,
                        comment='ACCOUNT_TOPUP',
                        trans_id=f"TXN-{uuid.uuid4().hex[:4].upper()}",
                        reference=f"REF-{uuid.uuid4().hex[:4].upper()}",
                        phone_number=member.phone_number,
                    )
                    top_up_transaction.save()

                    return redirect('list_transactions')

            # Form is valid, and the transaction has been processed, render the form again
            return redirect('list_transactions')

    else:
        form = TransactionForm()

    return render(request, 'transactions/transactions_form.html', {'form': form})


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


# Create View for Unmatched Transactions
@login_required
def add_unmatched_transaction(request):
    if request.method == 'POST':
        form = UnmatchedTransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('unmatched_transactions_list')
    else:
        form = UnmatchedTransactionForm()
    return render(
        request,
        'unmatched_transactions/unmatched_transactions_form.html',
        {'form': form}
    )


# List all unmatched transactions
@login_required
def unmatched_transactions_list(request):
    query = request.GET.get('search', '').strip()
    if query:
        transactions = UnmatchedTransaction.objects.filter(
            Q(trans_id__icontains=query) |
            Q(reference__icontains=query) |
            Q(phone_number__icontains=query)
        )
    else:
        transactions = UnmatchedTransaction.objects.all()

    # Ensure consistent ordering
    transactions = transactions.order_by('-date')

    paginator = Paginator(transactions, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'unmatched_transactions/unmatched_transactions_list.html',
        {'page_obj': page_obj, 'search_query': query}
    )


# Update View for Unmatched Transactions
@login_required
def update_unmatched_transaction(request, pk):
    transaction = get_object_or_404(UnmatchedTransaction, pk=pk)
    if request.method == 'POST':
        form = UnmatchedTransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('unmatched_transactions_list')
    else:
        form = UnmatchedTransactionForm(instance=transaction)
    return render(
        request,
        'unmatched_transactions/unmatched_transactions_form.html',
        {'form': form, 'transaction': transaction}
    )


# Delete View for Unmatched Transactions
@login_required
def delete_unmatched_transaction(request, pk):
    transaction = get_object_or_404(UnmatchedTransaction, pk=pk)
    if request.method == 'POST':
        transaction.delete()
        return redirect('unmatched_transactions_list')

    return render(
        request,
        'unmatched_transactions/unmatched_transaction_delete.html',
        {'transaction': transaction}
    )


# Export transactions to PDF
@login_required
def export_transactions_pdf(request):
    query = request.GET.get('search', '').strip()
    if not query:
        return HttpResponse(
            "Search query is required to generate PDF.",
            status=400
        )

    transactions = Transaction.objects.filter(
        Q(member__member_number__icontains=query) |
        Q(trans_id__icontains=query) |
        Q(reference__icontains=query) |
        Q(phone_number__icontains=query)
    ).order_by('-date')

    if not transactions.exists():
        return HttpResponse(
            "No transactions found for the given query.",
            status=404
        )

    # Render HTML content
    context = {'transactions': transactions, 'query': query}
    html_content = render_to_string(
        'transactions/transactions_pdf.html',
        context
    )

    # Create PDF from HTML
    response = HttpResponse(content_type='application/pdf')
    response[
        'Content-Disposition'
    ] = f'attachment; filename="{query}_transactions.pdf"'

    # Convert HTML to PDF
    pisa_status = pisa.CreatePDF(html_content, dest=response)

    # Check if the PDF was successfully created
    if pisa_status.err:
        return HttpResponse("Error generating PDF", status=500)

    return response
