from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.contrib import messages
from .models import Member
from transactions.models import Transaction
from penalties.models import Penalty
from .forms import MemberForm


# List all members
def list_members(request):
    members = Member.objects.all()
    return render(request, 'members/members_list.html', {'members': members})


def member_detail(request, member_id):
    member = get_object_or_404(Member, id=member_id)

    # Fetch transactions and penalties
    transactions = Transaction.objects.filter(member=member).order_by('-date')
    penalties = Penalty.objects.filter(member=member).order_by('-date')

    # Calculate totals
    total_transactions = transactions.aggregate(
        total_amount=Sum('amount')
    )['total_amount'] or 0
    total_penalties = penalties.aggregate(
        total_amount=Sum('amount')
    )['total_amount'] or 0
    penalties_paid = penalties.filter(
        is_paid=True
    ).aggregate(total_amount=Sum('amount'))['total_amount'] or 0
    penalties_unpaid = total_penalties - penalties_paid

    context = {
        'member': member,
        'transactions': transactions,
        'penalties': penalties,
        'total_transactions': total_transactions,
        'penalties_paid': penalties_paid,
        'penalties_unpaid': penalties_unpaid,
    }
    return render(request, 'members/member_detail.html', context)


# Add a new member
def add_member(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            new_member = form.save()
            messages.success(
                request,
                f'Member {new_member.first_name} '
                f'{new_member.last_name} added successfully.'
            )
            return redirect('list_members')
        else:
            messages.error(
                request,
                'There was an error adding the member. Please try again.'
            )
    else:
        form = MemberForm()
    return render(request, 'members/members_form.html', {'form': form})


# Update a member
def update_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    if request.method == 'POST':
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                f'Member {member.first_name} '
                f'{member.last_name} updated successfully.'
            )
            return redirect('member_detail', member_id=member.id)
        else:
            messages.error(
                request,
                'There was an error updating the member. Please try again.'
            )
    else:
        form = MemberForm(instance=member)
    return render(request, 'members/members_form.html', {'form': form})


# Delete a member
def delete_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    member_name = f"{member.first_name} {member.last_name}"
    member.delete()
    messages.success(request, f'Member {member_name} deleted successfully.')
    return redirect('list_members')
