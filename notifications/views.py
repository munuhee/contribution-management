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

import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import SendBulkSMSForm
from .sms_utils import send_sms
from .models import SentMessage
from members.models import Member

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)


@login_required
def send_bulk_sms(request):
    """
    View to send bulk SMS messages to all members.
    """
    if request.method == 'POST':
        form = SendBulkSMSForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']
            members = Member.objects.all()
            successful_count = 0
            failed_count = 0

            for member in members:
                if not member.phone_number:
                    logger.warning(f"Member {member.id} has no phone number.")
                    failed_count += 1
                    continue

                try:
                    response = send_sms(member.phone_number, message)
                    if response and response.status_code == 200:
                        response_data = response.json()
                        logger.info(
                            f"SMS sent successfully to {member.phone_number}."
                        )
                        successful_count += 1
                    else:
                        response_data = response.json() if response else {}
                        logger.error(
                            f"Failed to send SMS to {member.phone_number}: "
                            f"{response_data}"
                        )
                        failed_count += 1
                except Exception as e:
                    logger.exception(
                        f"Error sending SMS to {member.phone_number}: {e}"
                    )
                    failed_count += 1

            # Save the message summary in the database
            try:
                SentMessage.objects.create(
                    message=message,
                    response={
                        "successful": successful_count,
                        "failed": failed_count
                    }
                )
                logger.info(
                    f"Bulk SMS operation completed. "
                    f"{successful_count} succeeded, {failed_count} failed."
                )
            except Exception as e:
                logger.exception(f"Error saving message details: {e}")
                messages.error(
                    request,
                    "Error saving SMS details. Check logs."
                )

            messages.success(
                request,
                f"SMS messages sent. {successful_count}"
                f" succeeded, {failed_count} failed."
            )
            return redirect('list_sent_messages')
        else:
            logger.warning("Invalid form submission.")
    else:
        form = SendBulkSMSForm()

    return render(request, 'notifications/send_bulk_sms.html', {'form': form})


@login_required
def list_sent_messages(request):
    """
    View to list sent messages with pagination.
    """
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
