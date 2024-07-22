from django.shortcuts import render, redirect
from django.contrib import messages
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
                    status = 'Sent'
                    response_data = response.json()
                else:
                    status = 'Failed'
                    response_data = response.json() if response else {}

                # Save the sent message details
                SentMessage.objects.create(
                    message=message,
                    status=status,
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
    return render(
        request,
        'notifications/list_sent_messages.html',
        {'messages_list': messages_list}
    )
