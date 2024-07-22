from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Case
from .forms import CaseForm
# from notifications.sms_utils import send_sms


# List all cases
@login_required
def list_cases(request):
    cases = Case.objects.all()
    return render(request, 'cases/cases_list.html', {'cases': cases})


# Detail view for a specific case
@login_required
def detail_case(request, case_id):
    case = get_object_or_404(Case, id=case_id)
    return render(request, 'cases/case_detail.html', {'case': case})


# Add a new case
@login_required
def add_case(request):
    if request.method == 'POST':
        form = CaseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_cases')
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
            return redirect('list_cases')
    else:
        form = CaseForm(instance=case)
    return render(request, 'cases/cases_form.html', {'form': form})


# Delete a case
@login_required
def delete_case(request, case_id):
    case = get_object_or_404(Case, id=case_id)
    case.delete()
    return redirect('list_cases')
