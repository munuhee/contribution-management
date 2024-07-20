from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Penalty
from .forms import PenaltyForm


# List all penalties
def list_penalties(request):
    penalties = Penalty.objects.all()
    return render(
        request, 'penalties/penalties_list.html', {'penalties': penalties}
    )


# Add a new penalty
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
def delete_penalty(request, penalty_id):
    penalty = get_object_or_404(Penalty, id=penalty_id)
    penalty.delete()
    messages.success(request, 'Penalty deleted successfully!')
    return redirect('list_penalties')
