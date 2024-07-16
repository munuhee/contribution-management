import json
import base64
import requests
from django.views import View
from django.http import JsonResponse
from django.conf import settings
from transactions.models import Transaction, UnmatchedTransactions
from members.models import Member


def get_access_token():
    try:
        api_key = (
            f"{settings.MPESA_CONSUMER_KEY}:{settings.MPESA_CONSUMER_SECRET}"
        )
        encoded_key = base64.b64encode(api_key.encode()).decode()

        headers = {
            'Authorization': f'Basic {encoded_key}',
            'Content-Type': 'application/json'
        }

        response = requests.get(settings.MPESA_AUTH_URL, headers=headers)
        response.raise_for_status()
        return response.json().get('access_token')
    except requests.RequestException as e:
        print(f"Error obtaining access token: {e}")
        return None


def register_urls():
    access_token = get_access_token()
    if not access_token:
        print("Failed to obtain access token")
        return

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    payload = {
        "ShortCode": settings.MPESA_SHORTCODE,
        "ResponseType": "Completed",
        "ConfirmationURL": settings.CONFIRMATION_URL,
        "ValidationURL": settings.VALIDATION_URL,
    }

    response = requests.post(
        settings.MPESA_REGISTER_URL,
        headers=headers,
        data=json.dumps(payload)
    )
    print(response.text.encode('utf8'))


class MpesaCallbackView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse(
                {"status": "error", "message": "Invalid JSON data"},
                status=400
            )

        transaction_type = data.get("TransactionType")

        if transaction_type == "PayBill":
            self.handle_payment(data)

        return JsonResponse({"status": "success"}, status=200)

    def handle_payment(self, data):
        trans_id = data.get("TransID")
        trans_amount = float(data.get("TransAmount", 0))
        bill_ref_number = data.get("BillRefNumber")
        msisdn = data.get("MSISDN")

        try:
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
