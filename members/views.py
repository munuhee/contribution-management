from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Member
from transactions.models import Transaction
from penalties.models import Penalty
from .forms import MemberForm


@login_required
def list_members(request):
    query = request.GET.get('search', '').strip()  # Get the search query from the request
    if query:
        # Filter members based on the query
        members = Member.objects.filter(
            first_name__icontains=query
        ) | Member.objects.filter(
            last_name__icontains=query
        ) | Member.objects.filter(
            phone_number__icontains=query
        ) | Member.objects.filter(
            member_number__icontains=query
        )
    else:
        members = Member.objects.all()

    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(members, 10)
    try:
        members = paginator.page(page)
    except PageNotAnInteger:
        members = paginator.page(1)
    except EmptyPage:
        members = paginator.page(paginator.num_pages)

    return render(request, 'members/members_list.html', {
        'members': members,
        'search_query': query
    })

@login_required
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
@login_required
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
@login_required
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
@login_required
def delete_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    member_name = f"{member.first_name} {member.last_name}"
    member.delete()
    messages.success(request, f'Member {member_name} deleted successfully.')
    return redirect('list_members')
