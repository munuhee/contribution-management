from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Penalty
from .forms import PenaltyForm


@login_required
def list_penalties(request):
    query = request.GET.get('search', '').strip()
    if query:
        penalties = Penalty.objects.filter(
            Q(member__member_number__icontains=query) |
            Q(case__case_number__icontains=query) |
            Q(amount__icontains=query) |
            Q(is_paid__icontains=query)
        )
    else:
        penalties = Penalty.objects.all()

    if query.lower() in ['true', 'false']:
        penalties = penalties | Penalty.objects.filter(
            is_paid=query.lower() == 'true'
        )

    # Ensure consistent ordering
    penalties = penalties.order_by('-date')

    # Pagination
    paginator = Paginator(penalties, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'penalties/penalties_list.html',
        {'penalties': page_obj,
         'search_query': query}
    )


# Add a new penalty
@login_required
def add_penalty(request):
    if request.method == 'POST':
        form = PenaltyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Penalty added successfully!')
            return redirect('list_penalties')
    else:
        form = PenaltyForm()
    return render(request, 'penalties/penalties_form.html', {'form': form})


# Update a penalty
@login_required
def update_penalty(request, penalty_id):
    penalty = get_object_or_404(Penalty, id=penalty_id)
    if request.method == 'POST':
        form = PenaltyForm(request.POST, instance=penalty)
        if form.is_valid():
            form.save()
            messages.success(request, 'Penalty updated successfully!')
            return redirect('list_penalties')
    else:
        form = PenaltyForm(instance=penalty)
    return render(request, 'penalties/penalties_form.html', {'form': form})


# Delete a penalty
@login_required
def delete_penalty(request, penalty_id):
    penalty = get_object_or_404(Penalty, id=penalty_id)
    penalty.delete()
    messages.success(request, 'Penalty deleted successfully!')
    return redirect('list_penalties')
