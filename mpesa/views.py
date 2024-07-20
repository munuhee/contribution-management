import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from decimal import Decimal
from django.views import View
from transactions.models import Transaction, UnmatchedTransactions
from penalties.models import Penalty
from members.models import Member


@method_decorator(csrf_exempt, name='dispatch')
class MpesaValidationView(View):
    def post(self, request, *args, **kwargs):
        pass


@method_decorator(csrf_exempt, name='dispatch')
class MpesaConfirmationView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
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
        bill_ref_number = data.get("BillRefNumber")
        msisdn = data.get("MSISDN")

        try:
            if bill_ref_number.endswith("P"):
                member_number = bill_ref_number[:-1]
                member = Member.objects.get(member_number=member_number)

                Transaction.objects.create(
                    member=member,
                    trans_id=trans_id,
                    amount=trans_amount,
                    phone_number=msisdn,
                )

                member.account_balance += trans_amount
                member.save()

                # Handle the penalty payment
                penalties = Penalty.objects.filter(
                    member=member, is_paid=False
                ).order_by('date')
                remaining_amount = trans_amount

                for penalty in penalties:
                    if remaining_amount >= penalty.amount:
                        remaining_amount -= penalty.amount
                        penalty.is_paid = True
                        penalty.save()
                    else:
                        penalty.amount -= remaining_amount
                        penalty.save()
                        remaining_amount = 0
                        break
            else:
                member = Member.objects.get(member_number=bill_ref_number)
                Transaction.objects.create(
                    member=member,
                    trans_id=trans_id,
                    amount=trans_amount,
                    phone_number=msisdn,
                )

                member.account_balance += trans_amount
                member.save()

            # Optionally, send SMS notification here
        except Member.DoesNotExist:
            UnmatchedTransactions.objects.create(
                trans_id=trans_id,
                amount=trans_amount,
                phone_number=msisdn,
            )
