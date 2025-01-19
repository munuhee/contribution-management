"""
Handles SMS notifications and tracking for the Django application.

This module provides views for sending bulk SMS messages to members and
viewing the history of sent messages. It integrates with Africa's Talking API
to send messages and manages message tracking using the `SentMessage` model.

Key Views:
1. `send_bulk_sms`: Sends a custom message to all members and logs the
   status of each SMS (sent or failed) in the database.
2. `list_sent_messages`: Displays a paginated list of all sent messages,
   including their status and other details.
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import SendBulkSMSForm
from .sms_utils import send_sms
from .models import SentMessage
from members.models import Member


@login_required
def send_bulk_sms(request):
    if request.method == 'POST':
        form = SendBulkSMSForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            members = Member.objects.all()

            for member in members:
                response = send_sms(member.phone_number, message)

                if response and response.status_code == 200:
                    response_data = response.json()
                else:
                    response_data = response.json() if response else {}

            # Save the sent message details
            SentMessage.objects.create(
                message=message,
                response=response_data
            )

            messages.success(
                request, 'SMS messages have been sent successfully.'
            )
            return redirect('list_sent_messages')
    else:
        form = SendBulkSMSForm()

    return render(request, 'notifications/send_bulk_sms.html', {'form': form})


@login_required
def list_sent_messages(request):
    messages_list = SentMessage.objects.all().order_by('-sent_at')

    # Pagination
    paginator = Paginator(messages_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'notifications/list_sent_messages.html',
        {'page_obj': page_obj}
    )
