import json
import logging
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
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
        client_ip = request.META.get('REMOTE_ADDR')

        # Check if the request's IP is in the whitelist
        if client_ip not in WHITELISTED_IPS:
            logger.error(f"Request from IP {client_ip} is not whitelisted.")
            return JsonResponse(
                {"status": "error", "message": "IP not whitelisted"},
                status=403
            )

        data = self.parse_json_data(request)
        if not data:
            return JsonResponse(
                {"status": "error", "message": "Invalid JSON data"},
                status=400
            )

        transaction_type = data.get("TransactionType")
        if transaction_type == "Pay Bill":
            self.handle_payment(data)

        return JsonResponse({"status": "success"}, status=200)

    def parse_json_data(self, request):
        """Parse JSON data from the request body."""
        try:
            return json.loads(request.body)
        except json.JSONDecodeError:
            logger.error("Invalid JSON data received")
            return None

    def handle_payment(self, data):
        trans_id = data.get("TransID")
        trans_amount = Decimal(data.get("TransAmount", 0))
        bill_ref_number = data.get("BillRefNumber").upper()
        msisdn = data.get("MSISDN")

        msisdn = self.format_msisdn(msisdn)

        try:
            if bill_ref_number.endswith("P"):
                logger.info("Penalty payment detected")
                # Remove the "P" from the bill reference number
                bill_ref_number = bill_ref_number[:-1]
                self.handle_penalty_payment(
                    data, trans_id, trans_amount,
                    bill_ref_number, msisdn
                )
            else:
                logger.info("Regular payment detected")
                self.handle_regular_payment(
                    data, trans_id,
                    trans_amount, bill_ref_number,
                    msisdn
                )
        except Exception as e:
            logger.error(f"Error processing payment: {e}")
            return JsonResponse(
                {"status": "error", "message": "Error processing payment"},
                status=500
            )

    def format_msisdn(self, msisdn):
        """Ensure MSISDN starts with a plus sign."""
        return f"+{msisdn}" if not msisdn.startswith("+") else msisdn

    def handle_regular_payment(
        self, data, trans_id, trans_amount, bill_ref_number, msisdn
    ):
        """Handle regular payments (non-penalty)."""
        try:
            member = self.get_member_by_bill_ref(bill_ref_number)
            if member:
                self.settle_invoices(member, trans_amount, trans_id, msisdn)
            else:
                self.create_unmatched_transaction(
                    trans_id,
                    trans_amount,
                    msisdn
                )
        except Exception as e:
            logger.error(f"Error handling regular payment: {e}")

    def get_member_by_bill_ref(self, bill_ref_number):
        """Retrieve a member based on the bill reference number."""
        return Member.objects.filter(member_number=bill_ref_number).first()

    def create_unmatched_transaction(self, trans_id, trans_amount, msisdn):
        """Create an unmatched transaction and send an SMS notification."""
        unmatched_transaction = UnmatchedTransaction(
            trans_id=trans_id,
            amount=trans_amount,
            phone_number=msisdn,
            comment="Payment could not be matched to any account"
        )
        unmatched_transaction.save()
        message = (
            "Your payment could not be matched to any account."
            " Please contact support."
        )
        send_sms(to=msisdn, message=message)

    def handle_penalty_payment(
        self, data, trans_id, trans_amount, bill_ref_number, msisdn
    ):
        """
        Handle penalty payments
        by processing multiple penalties in order.
        """
        try:
            member = self.get_member_by_bill_ref(bill_ref_number)
            if member:
                logger.info("Member found for penalty payment")
                # Pay penalties first
                remaining_amount = self.pay_penalties_if_any(
                    member, trans_amount, trans_id, msisdn
                )

                # Use remaining amount to settle invoices if applicable
                if remaining_amount > 0:
                    self.settle_invoices(
                        member, remaining_amount, trans_id, msisdn
                    )
            else:
                logger.info("Member not found for penalty payment")
                self.create_unmatched_transaction(
                    trans_id, trans_amount, msisdn
                )
        except Exception as e:
            logger.error(f"Error handling penalty payment: {e}")

    def get_oldest_unpaid_penalty(self, bill_ref_number):
        """Retrieve the oldest unpaid penalty record."""
        return Penalty.objects.filter(
            member__member_number=bill_ref_number, is_paid=False
        ).order_by('date').first()

    def process_penalty_payment(self, penalty, trans_id, trans_amount, msisdn):
        """Process a penalty payment."""
        penalty.is_paid = True
        penalty.save()

        # Create penalty payment transaction
        Transaction.objects.create(
            member=penalty.member,
            amount=penalty.amount,
            comment='PENALTY_PAYMENT',
            trans_id=trans_id,
            phone_number=msisdn,
            invoice=None if penalty.invoice is None else penalty.invoice
        )

        # Send SMS confirmation
        message = (
            f"Penalty payment of {penalty.amount} successfully processed."
        )
        send_sms(to=msisdn, message=message)

    def pay_penalties_if_any(self, member, amount, trans_id, msisdn):
        """Pay penalties sequentially (oldest first)"""
        penalties = Penalty.objects.filter(
            member=member, is_paid=False
        ).order_by('date')  # Oldest penalties first

        remaining_amount = amount
        for penalty in penalties:
            if remaining_amount <= 0:
                break

            # Pay off the penalty completely or partially
            if penalty.amount <= remaining_amount:
                paid_amount = penalty.amount
                penalty.is_paid = True
                penalty.save()
            else:
                paid_amount = remaining_amount
                penalty.amount -= remaining_amount
                penalty.save()

            # Record the transaction for the penalty payment
            Transaction.objects.create(
                member=member,
                amount=paid_amount,
                comment='PENALTY_PAYMENT',
                trans_id=trans_id,
                phone_number=msisdn,
                invoice=penalty.invoice
            )

            # Send SMS confirmation for each penalty payment
            send_sms(
                to=msisdn,
                message=(
                    f"Penalty payment of {paid_amount} successfully processed."
                )
            )

            # Deduct the paid amount from the remaining amount
            remaining_amount -= paid_amount

        return remaining_amount

    def settle_invoices(self, member, amount, trans_id, msisdn):
        """Settle unpaid invoices for a member, starting from the oldest."""
        try:
            outstanding_invoices = Invoice.objects.filter(
                member=member, is_settled=False
            ).order_by('issue_date')  # Oldest invoices first

            remaining_amount = amount
            for invoice in outstanding_invoices:
                if remaining_amount <= 0:
                    break

                if invoice.outstanding_balance <= remaining_amount:
                    # Fully settle the invoice
                    self.settle_full_invoice(
                        invoice, remaining_amount,
                        trans_id, msisdn, member
                    )
                    remaining_amount -= invoice.outstanding_balance
                else:
                    # Partially settle the invoice
                    self.settle_partial_invoice(
                        invoice, remaining_amount,
                        trans_id, msisdn, member
                    )
                    remaining_amount = 0

            # Ensure that a top-up only happens if there's
            # ACTUALLY extra money left
            if remaining_amount > 0 and any(
                inv.outstanding_balance > 0 for inv in outstanding_invoices
            ):
                self.top_up_account_balance(
                    remaining_amount, trans_id, msisdn, member
                )

        except Exception as e:
            logger.error(f"Error settling invoices: {e}")

    def settle_full_invoice(
        self, invoice, amount_remaining, trans_id, msisdn, member
    ):
        """Fully settle an invoice."""
        paid_amount = invoice.outstanding_balance
        invoice.outstanding_balance = 0
        invoice.is_settled = True
        invoice.save()

        Transaction.objects.create(
            member=member,
            amount=paid_amount,
            comment='INVOICE_PAYMENT',
            trans_id=trans_id,
            phone_number=msisdn,
            invoice=invoice
        )
        # Update the member's account balance
        member.account_balance += paid_amount
        member.save()

        send_sms(
            to=msisdn,
            message=f"Invoice payment of {paid_amount} successfully processed."
        )

    def settle_partial_invoice(
        self, invoice, amount_remaining, trans_id, msisdn, member
    ):
        """Partially settle an invoice."""
        paid_amount = amount_remaining
        invoice.outstanding_balance -= paid_amount
        invoice.save()

        Transaction.objects.create(
            member=member,
            amount=paid_amount,
            comment='INV_PARTIAL_PAY',
            trans_id=trans_id,
            phone_number=msisdn,
            invoice=invoice
        )

        send_sms(
            to=msisdn,
            message=(
                f"Partial invoice payment of {paid_amount}"
                f"successfully processed."
            )
        )

    def top_up_account_balance(
        self, amount_remaining,
        trans_id, msisdn, member
    ):
        """Top up the member's account balance."""
        member.account_balance += amount_remaining
        member.save()

        Transaction.objects.create(
            member=member,
            amount=amount_remaining,
            comment='ACCOUNT_TOPUP',
            trans_id=trans_id,
            phone_number=msisdn
        )

        send_sms(
            to=msisdn,
            message=f"Account topped up with {amount_remaining} successfully."
        )
