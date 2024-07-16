from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Member
from .forms import MemberForm


# List all members
def list_members(request):
    members = Member.objects.all()
    return render(request, 'members/list.html', {'members': members})


# Add a new member
def add_member(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_members')
    else:
        form = MemberForm()
    return render(request, 'members/form.html', {'form': form})


# Update a member
def update_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    if request.method == 'POST':
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect('list_members')
    else:
        form = MemberForm(instance=member)
    return render(request, 'members/form.html', {'form': form})


# Delete a member
def delete_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    member.delete()
    return redirect('list_members')
