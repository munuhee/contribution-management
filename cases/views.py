from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from members.models import Member
from transactions.models import Invoice
from .models import Case
from .forms import CaseForm


# List all cases
@login_required
def list_cases(request):
    query = request.GET.get('search', '').strip()
    if query:
        # Filter cases based on the query
        cases = Case.objects.filter(
            case_number__icontains=query
        ) | Case.objects.filter(
            description__icontains=query
        )
    else:
        cases = Case.objects.all()

    # Ensure consistent ordering
    cases = cases.order_by('-created_at')

    # Pagination
    paginator = Paginator(cases, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'cases/cases_list.html', {
        'page_obj': page_obj,
        'search_query': query
    })


# Detail view for a specific case
@login_required
def detail_case(request, case_id):
    case = get_object_or_404(Case, id=case_id)
    return render(request, 'cases/case_detail.html', {'case': case})


@login_required
def add_case(request):
    if request.method == 'POST':
        form = CaseForm(request.POST)
        if form.is_valid():
            case = form.save()
            members = Member.objects.all()
            for member in members:
                # Create invoice
                invoice = Invoice.objects.create(
                    invoice_number=f"INV{case.case_number}{member.member_number}",
                    member=member,
                    case=case,
                    due_date=case.deadline,
                    amount=case.amount,
                    description=f"Invoice for case {case.case_number}"
                )
                # Attempt to settle the invoice
                if member.settle_invoice(invoice):
                    messages.success(
                        request,
                        f"Invoice for member {member.first_name} {member.last_name} settled using account balance."
                    )
                else:
                    messages.warning(
                        request,
                        f"Invoice for member {member.first_name} {member.last_name} created but not settled due to insufficient balance."
                    )
            messages.success(request, 'Case added and invoices generated successfully!')
            return redirect('list_cases')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CaseForm()
    return render(request, 'cases/cases_form.html', {'form': form})


# Update a case
@login_required
def update_case(request, case_id):
    case = get_object_or_404(Case, id=case_id)
    if request.method == 'POST':
        form = CaseForm(request.POST, instance=case)
        if form.is_valid():
            form.save()
            messages.success(request, 'Case updated successfully!')
            return redirect('list_cases')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CaseForm(instance=case)
    return render(request, 'cases/cases_form.html', {'form': form})


# Delete a case
@login_required
def delete_case(request, case_id):
    case = get_object_or_404(Case, id=case_id)
    case.delete()
    messages.success(request, 'Case deleted successfully!')
    return redirect('list_cases')
