import uuid

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.template.loader import render_to_string

from xhtml2pdf import pisa

from penalties.models import Penalty
from .models import Transaction, UnmatchedTransaction, Invoice
from .forms import TransactionForm, UnmatchedTransactionForm, InvoiceForm


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


@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.trans_id = f"TXN{uuid.uuid4().hex[:6].upper()}"

            if transaction.comment in ['INVOICE_PAYMENT', 'INV_PARTIAL_PAY'] and transaction.member:
                member = transaction.member
                outstanding_invoices = Invoice.objects.filter(
                    member=member, is_settled=False
                ).order_by('issue_date')

                amount_remaining = transaction.amount
                for invoice in outstanding_invoices:
                    if amount_remaining <= 0:
                        break

                    if invoice.outstanding_balance <= amount_remaining:
                        # Fully settle the invoice
                        paid_amount = invoice.outstanding_balance
                        amount_remaining -= paid_amount
                        invoice.outstanding_balance = 0
                        invoice.is_settled = True
                        invoice.save()

                        # Log the payment transaction
                        Transaction.objects.create(
                            member=member,
                            amount=paid_amount,
                            comment='INVOICE_PAYMENT',
                            trans_id=f"INV-{uuid.uuid4().hex[:6].upper()}",
                            phone_number="-",
                            invoice=invoice,
                        )

                        # Update member's account balance
                        member.account_balance += paid_amount
                        member.save()
                    else:
                        # Partially settle the invoice
                        paid_amount = amount_remaining
                        invoice.outstanding_balance -= paid_amount
                        amount_remaining = 0
                        invoice.save()

                        # Log the partial payment transaction
                        Transaction.objects.create(
                            member=member,
                            amount=paid_amount,
                            comment='INV_PARTIAL_PAY',
                            trans_id=f"INV-{uuid.uuid4().hex[:6].upper()}",
                            phone_number="-",
                            invoice=invoice,
                        )

                        # Update member's account balance
                        member.account_balance += paid_amount
                        member.save()

                # Handle any remaining amount as a top-up
                if amount_remaining > 0:
                    member.account_balance += amount_remaining
                    member.save()

                    Transaction.objects.create(
                        member=member,
                        amount=amount_remaining,
                        comment='ACCOUNT_TOPUP',
                        trans_id=f"TXN-{uuid.uuid4().hex[:6].upper()}",
                        phone_number=member.phone_number,
                    )

                # Skip saving the main transaction to avoid duplication
                return redirect('list_transactions')

            elif transaction.comment == 'ACCOUNT_TOPUP' and transaction.member:
                # Handle Account Top-Up and invoice payment logic
                member = transaction.member
                top_up_amount = transaction.amount

                # First, check for outstanding invoices
                outstanding_invoices = Invoice.objects.filter(
                    member=member, is_settled=False
                ).order_by('issue_date')

                amount_remaining = top_up_amount
                for invoice in outstanding_invoices:
                    if amount_remaining <= 0:
                        break

                    if invoice.outstanding_balance <= amount_remaining:
                        # Fully settle the invoice
                        paid_amount = invoice.outstanding_balance
                        amount_remaining -= paid_amount
                        invoice.outstanding_balance = 0  # Set outstanding balance to zero
                        invoice.is_settled = True  # Mark invoice as settled
                        invoice.save()

                        # Log the payment transaction
                        Transaction.objects.create(
                            member=member,
                            amount=paid_amount,
                            comment='INVOICE_PAYMENT',
                            trans_id=f"INV-{uuid.uuid4().hex[:6].upper()}",
                            phone_number="-",
                            invoice=invoice,
                        )

                        # Update member's account balance
                        member.account_balance += paid_amount
                        member.save()
                    else:
                        # Partially settle the invoice
                        paid_amount = amount_remaining
                        invoice.outstanding_balance -= paid_amount
                        amount_remaining = 0
                        invoice.save()

                        # Log the partial payment transaction
                        Transaction.objects.create(
                            member=member,
                            amount=paid_amount,
                            comment='INV_PARTIAL_PAY',
                            trans_id=f"INV-{uuid.uuid4().hex[:6].upper()}",
                            phone_number="-",
                            invoice=invoice,
                        )

                        # Update member's account balance
                        member.account_balance += paid_amount
                        member.save()

                # If there's remaining amount, add it to the account balance
                if amount_remaining > 0:
                    member.account_balance += amount_remaining
                    member.save()

                    # Log the remaining amount as a top-up
                    Transaction.objects.create(
                        member=member,
                        amount=amount_remaining,
                        comment='ACCOUNT_TOPUP',
                        trans_id=f"TXN-{uuid.uuid4().hex[:6].upper()}",
                        phone_number=member.phone_number,
                    )

                return redirect('list_transactions')

            elif transaction.comment == 'PENALTY_PAYMENT' and transaction.member:
                member = transaction.member
                remaining_amount = transaction.amount
                penalties = Penalty.objects.filter(member=member, is_paid=False).order_by('id')

                for penalty in penalties:
                    if remaining_amount <= 0:
                        break

                    if penalty.amount <= remaining_amount:
                        remaining_amount -= penalty.amount
                        penalty.is_paid = True
                        penalty.save()

                        Transaction.objects.create(
                            member=member,
                            amount=penalty.amount,
                            comment='PENALTY_PAYMENT',
                            trans_id=f"PEN-{uuid.uuid4().hex[:6].upper()}",
                            phone_number="-",
                            invoice=(
                                None if penalty.invoice is None else penalty.invoice
                            ),
                        )
                    else:
                        penalty.amount -= remaining_amount
                        penalty.save()
                        remaining_amount = 0

                if remaining_amount > 0:
                    member.account_balance += remaining_amount
                    member.save()

                    Transaction.objects.create(
                        member=member,
                        amount=remaining_amount,
                        comment='ACCOUNT_TOPUP',
                        trans_id=f"TXN-{uuid.uuid4().hex[:6].upper()}",
                        phone_number=member.phone_number,
                    )

                # Skip saving the main transaction to avoid duplication
                return redirect('list_transactions')

            # Save the main transaction only for unrelated cases
            transaction.save()
            return redirect('list_transactions')

    else:
        form = TransactionForm()

    return render(
        request,
        'transactions/transactions_form.html',
        {'form': form}
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


# Create Invoice
def invoice_create(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save(commit=False)
            case = invoice.case
            member = invoice.member

            # Ensure both case and member are available
            if not case or not member:
                messages.error(
                    request,
                    "Failed: Missing associated case or member."
                )
                return redirect('invoice_list')

            # Generate a unique invoice number
            base_invoice_number = (
                f"INV-{case.case_number}-{member.member_number}"
            )
            invoice.invoice_number = base_invoice_number
            counter = 1

            # Ensure uniqueness of the invoice_number
            while Invoice.objects.filter(
                invoice_number=invoice.invoice_number
            ).exists():
                invoice.invoice_number = f"{base_invoice_number}-{counter}"
                counter += 1

            invoice.save()

            # Create the initial transaction for invoice creation
            Transaction.objects.create(
                member=member,
                amount=invoice.amount,
                comment='INVOICE_CREATION',
                trans_id=invoice.invoice_number,
                reference=f"REF-{uuid.uuid4().hex[:12].upper()}",
                phone_number=member.phone_number,
            )
            messages.success(request, "Invoice created successfully!")

            # Check if the member's balance is sufficient for payment
            if member.account_balance >= invoice.amount:
                # Deduct balance and mark invoice as paid
                member.account_balance -= invoice.amount
                member.save()

                # Create a transaction to record payment
                Transaction.objects.create(
                    member=member,
                    invoice=invoice,
                    amount=invoice.amount,
                    comment='INVOICE_PAYMENT',
                    trans_id=f"PAY-{invoice.invoice_number}",
                    reference=f"REF-{uuid.uuid4().hex[:8].upper()}",
                    phone_number=member.phone_number,
                )

                # Mark invoice as settled
                invoice.is_settled = True
                invoice.save()
                messages.success(
                    request,
                    "Invoice payment recorded successfully!"
                )
            else:
                # Handle insufficient balance
                member.account_balance -= invoice.amount
                member.save()
                messages.warning(
                    request,
                    "Invoice created but member has insufficient balance."
                )

            return redirect('invoice_list')
        else:
            # Handle form validation errors
            messages.error(
                request,
                "There was an error with your submission. Please correct it."
            )
    else:
        form = InvoiceForm()

    return render(
        request,
        'invoices/invoice_form.html',
        {'form': form}
    )


# Retrieve Invoice (List View)
def invoice_list(request):
    invoices = Invoice.objects.all()
    paginator = Paginator(invoices, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'invoices/invoice_list.html',
        {'page_obj': page_obj}
    )


# Retrieve Invoice (Detail View)
def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    return render(
        request,
        'invoices/invoice_detail.html',
        {'invoice': invoice}
    )


# Update Invoice
def invoice_update(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            form.save()
            return redirect('invoice_list')
    else:
        form = InvoiceForm(instance=invoice)
    return render(request, 'invoices/invoice_form.html', {'form': form})


# Delete Invoice
@login_required
def invoice_delete(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    invoice.delete()
    return redirect('invoice_list')
