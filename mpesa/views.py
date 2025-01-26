"""
Handles MPESA payment validation and confirmation in Django.

This module provides views for processing MPESA payment notifications:
1. `MpesaValidationView`: A placeholder for handling payment
validation requests.
2. `MpesaConfirmationView`: Processes payment confirmations,
updates member accounts, and handles penalties.

Key Features:
- Matches payments to members using the bill reference number.
- Updates member balances and pays off penalties if applicable.
- Saves unmatched transactions for later review.

Dependencies:
- CSRF exemption for handling external MPESA requests.
- Models:
  - `Transaction` for storing successful payments.
  - `UnmatchedTransaction` for payments that can’t be matched to a member.
  - `Penalty` for handling unpaid penalties.
  - `Member` for managing member accounts.

"""

import json
import logging
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from decimal import Decimal
from django.views import View
from transactions.models import Transaction, UnmatchedTransaction, Invoice
from penalties.models import Penalty
from members.models import Member
from notifications.sms_utils import send_sms
from django.conf import settings

# Set up logging
logger = logging.getLogger(__name__)

# Define the whitelist for IP addresses
WHITELISTED_IPS = settings.WHITELISTED_IPS


@method_decorator(csrf_exempt, name='dispatch')
class MpesaValidationView(View):
    def post(self, request, *args, **kwargs):
        pass


@method_decorator(csrf_exempt, name='dispatch')
class MpesaConfirmationView(View):
    def post(self, request, *args, **kwargs):
        # Check if the request's IP is in the whitelist
        client_ip = request.META.get('REMOTE_ADDR')
        if client_ip not in WHITELISTED_IPS:
            logger.error(f"Request from IP {client_ip} is not whitelisted.")
            return JsonResponse(
                {"status": "error", "message": "IP not whitelisted"},
                status=403
            )
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            logger.error("Invalid JSON data received")
            return JsonResponse(
                {"status": "error", "message": "Invalid JSON data"},
                status=400
            )

        transaction_type = data.get("TransactionType")

        if transaction_type == "Pay Bill":
            self.handle_payment(data)

        return JsonResponse({"status": "success"}, status=200)

    def handle_payment(self, data):
        trans_id = data.get("TransID")
        trans_amount = Decimal(data.get("TransAmount", 0))
        bill_ref_number = data.get("BillRefNumber").upper()
        msisdn = data.get("MSISDN")

        # Ensure MSISDN starts with a plus sign
        if not msisdn.startswith("+"):
            msisdn = f"+{msisdn}"

        try:
            member = None

            if bill_ref_number.endswith("P"):
                # Handle payments for penalties
                member_number = bill_ref_number[:-1]
                member = Member.objects.get(member_number=member_number)
                logger.info(
                    "Processing penalty payment for member: %s",
                    member_number
                )

                remaining_amount = trans_amount
                penalties = Penalty.objects.filter(
                    member=member,
                    is_paid=False
                ).order_by('date')
                total_penalties_paid = 0

                for penalty in penalties:
                    if remaining_amount >= penalty.amount:
                        remaining_amount -= penalty.amount
                        total_penalties_paid += penalty.amount
                        penalty.is_paid = True
                        penalty.save()

                        Transaction.objects.create(
                            member=member,
                            trans_id=trans_id,
                            amount=penalty.amount,
                            phone_number=msisdn,
                            comment="Penalty Payment",
                        )
                    else:
                        break

                if remaining_amount > 0:
                    # Settle invoices in the correct order
                    self.settle_invoices(
                        member,
                        remaining_amount,
                        trans_id, msisdn
                    )
            else:
                # Handle payments without "P"
                member = Member.objects.get(member_number=bill_ref_number)
                logger.info(
                    "Processing payment for invoices for member: %s",
                    bill_ref_number
                )

                # Settle the oldest invoices first
                remaining_amount = self.settle_invoices(
                    member,
                    trans_amount,
                    trans_id,
                    msisdn
                )

            # Update member account balance if there is remaining amount
            if member and remaining_amount > 0:
                member.account_balance += remaining_amount
                member.save()
                Transaction.objects.create(
                    member=member,
                    trans_id=trans_id,
                    amount=remaining_amount,
                    phone_number=msisdn,
                    comment="Account Top-up",
                )

                message = (
                    f"Dear {member.first_name}, "
                    f"your payment of {trans_amount:.2f} has been received. "
                    f"Your updated account balance is {
                        member.account_balance:.2f
                    }."
                )
                send_sms(to=msisdn, message=message)

        except Member.DoesNotExist:
            logger.error(
                "Member not found for BillRefNumber: %s",
                bill_ref_number
            )
            UnmatchedTransaction.objects.create(
                trans_id=trans_id,
                amount=trans_amount,
                phone_number=msisdn,
            )
            message = (
                "Your payment could not be matched to any account. "
                "Please contact support for assistance."
            )
            send_sms(to=msisdn, message=message)

    def settle_invoices(self, member, amount, trans_id, msisdn):
        """Settle unpaid invoices for a member starting from the oldest."""
        remaining_amount = amount
        invoices = Invoice.objects.filter(
            member=member, is_settled=False
        ).order_by('issue_date')

        for invoice in invoices:
            if remaining_amount >= invoice.amount:
                remaining_amount -= invoice.amount
                invoice.is_settled = True
                invoice.save()

                Transaction.objects.create(
                    member=member,
                    trans_id=trans_id,
                    amount=invoice.amount,
                    invoice=invoice,
                    phone_number=msisdn,
                    comment="Invoice Payment",
                )
            else:
                break

        return remaining_amount
