from django.shortcuts import render
from django.db.models import Sum
from members.models import Member
from transactions.models import Transaction
from cases.models import Case


def dashboard_view(request):
    admin = {'name': 'Jone Doe', 'role': 'Admin'}
    total_members = Member.objects.count()
    total_transactions = Transaction.objects.count()
    total_amount = Transaction.objects.aggregate(
        Sum('amount'))['amount__sum'] or 0
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
