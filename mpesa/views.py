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
            # Determine if the payment is for a penalty or regular transaction
            if bill_ref_number.endswith("P"):
                # Handle payments for penalties
                self.handle_penalty_payment(
                    data,
                    trans_id,
                    trans_amount,
                    bill_ref_number,
                    msisdn
                )
            else:
                # Handle regular payments
                self.handle_regular_payment(
                    data,
                    trans_id,
                    trans_amount,
                    bill_ref_number,
                    msisdn
                )

        except Exception as e:
            logger.error(f"Error processing payment: {e}")
            return JsonResponse(
                {"status": "error", "message": "Error processing payment"},
                status=500
            )

    def handle_regular_payment(
        self, data, trans_id, trans_amount,
        bill_ref_number, msisdn
    ):
        """Handle payments that are not penalties."""
        try:
            try:
                # Look up the member using the bill reference number (or MSISDN if needed)
                member_number = bill_ref_number  # Assuming bill_ref_number is the member number
                member = Member.objects.filter(member_number=member_number).first()

                if member:
                    # Process the payment (settle invoices or top up account balance)
                    self.settle_invoices(member, trans_amount, trans_id, msisdn)
                else:
                    # Create an unmatched transaction if no member is found
                    UnmatchedTransaction.objects.create(
                        trans_id=trans_id,
                        amount=trans_amount,
                        phone_number=msisdn,
                        bill_ref_number=bill_ref_number,
                    )
                    message = (
                        "Your payment could not be matched to any account. "
                        "Please contact support for assistance."
                    )
                    send_sms(to=msisdn, message=message)

            except Exception as e:
                logger.error(f"Error handling regular payment: {e}")

    def handle_penalty_payment(
        self, data, trans_id,
        trans_amount, bill_ref_number, msisdn
    ):
        """Handle payments for penalties."""
        try:
            # Find the penalty record
            penalty = Penalty.objects.filter(
                invoice__invoice_number=bill_ref_number[:-1],
                is_paid=False
            ).first()

            if penalty:
                penalty.is_paid = True
                penalty.save()

                # Create a penalty payment transaction
                Transaction.objects.create(
                    member=penalty.member,
                    amount=penalty.amount,
                    comment='PENALTY_PAYMENT',
                    trans_id=trans_id,
                    phone_number=msisdn,
                    invoice=penalty.invoice
                )

                # Update member's account balance
                penalty.member.account_balance += penalty.amount
                penalty.member.save()

                # Send confirmation SMS to the user
                message = (
                    f"Penalty payment of {penalty.amount}"
                    f"successfully processed."
                )
                send_sms(to=msisdn, message=message)

            else:
                # If no matching penalty found, create an unmatched transaction
                UnmatchedTransaction.objects.create(
                    trans_id=trans_id,
                    amount=trans_amount,
                    phone_number=msisdn,
                )
                message = (
                    "Your penalty payment could not be matched to any account."
                    " Please contact support for assistance."
                )
                send_sms(to=msisdn, message=message)

        except Exception as e:
            logger.error(f"Error handling penalty payment: {e}")

    def settle_invoices(self, member, amount, trans_id, msisdn):
        """Settle unpaid invoices for a member starting from the oldest."""
        try:
            outstanding_invoices = Invoice.objects.filter(
                member=member, is_settled=False
            ).order_by('issue_date')

            amount_remaining = amount
            for invoice in outstanding_invoices:
                if amount_remaining <= 0:
                    break

                if invoice.outstanding_balance <= amount_remaining:
                    # Fully settle the invoice
                    paid_amount = invoice.outstanding_balance
                    amount_remaining -= paid_amount
                    invoice.outstanding_balance = 0
                    invoice.is_settled = True
                    invoice.save()

                    # Log the payment transaction
                    Transaction.objects.create(
                        member=member,
                        amount=paid_amount,
                        comment='INVOICE_PAYMENT',
                        trans_id=trans_id,
                        phone_number=msisdn,
                        invoice=invoice
                    )

                    # Update member's account balance
                    member.account_balance += paid_amount
                    member.save()
                else:
                    # Partially settle the invoice
                    paid_amount = amount_remaining
                    invoice.outstanding_balance -= paid_amount
                    amount_remaining = 0
                    invoice.save()

                    # Log the partial payment transaction
                    Transaction.objects.create(
                        member=member,
                        amount=paid_amount,
                        comment='INV_PARTIAL_PAY',
                        trans_id=trans_id,
                        phone_number=msisdn,
                        invoice=invoice
                    )

                    # Update member's account balance
                    member.account_balance += paid_amount
                    member.save()

            # Handle any remaining amount as a top-up
            if amount_remaining > 0:
                member.account_balance += amount_remaining
                member.save()

                Transaction.objects.create(
                    member=member,
                    amount=amount_remaining,
                    comment='ACCOUNT_TOPUP',
                    trans_id=trans_id,
                    phone_number=msisdn
                )

        except Exception as e:
            logger.error(f"Error settling invoices: {e}")
