from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import redirect, render

from .forms import LoginForm
from cases.models import Case
from members.models import Member
from transactions.models import Transaction


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect('dashboard_view')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'core/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('login')


def password_reset_done(request):
    messages.success(
        request,
        "An email has been sent with instructions to reset your password."
    )
    return redirect('login')


def password_reset_complete(request):
    messages.success(request, "Your password has been reset successfully.")
    return redirect('login')


@login_required
def dashboard_view(request):
    admin = {'name': 'Jone Doe', 'role': 'Admin'}
    total_members = Member.objects.count()
    total_transactions = Transaction.objects.count()
    total_amount = Transaction.objects.aggregate(
        Sum('amount'))['amount__sum'] or 0

    # Format the total_amount to two decimal places
    total_amount = f"{total_amount:.2f}"

    cases = Case.objects.all().order_by('-created_at')[:5]
    total_cases = Case.objects.count()

    context = {
        'admin': admin,
        'total_members': total_members,
        'total_transactions': total_transactions,
        'total_cases': total_cases,
        'total_amount': total_amount,
        'cases': cases,
    }
    return render(request, 'core/dashboard.html', context)
