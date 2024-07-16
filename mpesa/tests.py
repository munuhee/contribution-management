import json
from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
from .models import Member, Transaction

class MpesaPaymentTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.member = Member.objects.create(
            first_name="John",
            last_name="Doe",
            phone_number="254712345678",
            member_number="413",
            national_id="12345678",
            account_balance=1000.0
        )
        self.payment_url = reverse('mpesa_payment')
        self.callback_url = reverse('mpesa_callback')

    @patch('mpesa.views.requests.post')  # Mocking requests.post
    @patch('mpesa.views.MpesaPaymentView.get_access_token', return_value='fake_access_token')
    def test_mpesa_payment_success(self, mock_get_token, mock_post):
        mock_post.return_value.json.return_value = {
            "ResponseCode": "0",  # Assuming success response from Mpesa
            "ResponseDescription": "Success"
        }

        response = self.client.post(self.payment_url, {
            'phone_number': '254712345678',
            'amount': 500,
            'account_reference': '413'
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn("ResponseCode", response.json())
        self.assertEqual(response.json()["ResponseCode"], "0")

    def test_mpesa_callback_success(self):
        response_data = {
            "TransactionType": "PayBill",
            "TransID": "LK12345678",
            "TransTime": "2023-08-23T14:30:00+03:00",
            "TransAmount": "500",
            "BusinessShortCode": "601426",
            "BillRefNumber": "413",
            "MSISDN": "254712345678"
        }

        response = self.client.post(self.callback_url, json.dumps(response_data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        transaction = Transaction.objects.get(reference="LK12345678")
        self.assertEqual(transaction.amount, 500)
        self.assertEqual(transaction.member, self.member)
        self.assertEqual(self.member.account_balance, 1500.0)  # Updated balance

    def test_callback_invalid_member(self):
        response_data = {
            "TransactionType": "PayBill",
            "TransID": "LK12345678",
            "TransAmount": "500",
            "BillRefNumber": "999",  # Non-existent member number
            "MSISDN": "254712345678"
        }

        response = self.client.post(self.callback_url, json.dumps(response_data), content_type='application/json')

        self.assertEqual(response.status_code, 200)  # Handle gracefully
        self.assertEqual(Transaction.objects.count(), 0)  # No transaction created

class MpesaPaymentEdgeCasesTests(TestCase):
    @patch('mpesa.views.requests.post')
    @patch('mpesa.views.MpesaPaymentView.get_access_token', return_value='fake_access_token')
    def test_mpesa_payment_failure(self, mock_get_token, mock_post):
        mock_post.return_value.json.return_value = {
            "ResponseCode": "1",  # Assuming failure response from Mpesa
            "ResponseDescription": "Transaction failed"
        }

        response = self.client.post(self.payment_url, {
            'phone_number': '254712345678',
            'amount': 500,
            'account_reference': '413'
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn("ResponseCode", response.json())
        self.assertEqual(response.json()["ResponseCode"], "1")

    def test_invalid_account_reference(self):
        response = self.client.post(self.payment_url, {
            'phone_number': '254712345678',
            'amount': 500,
            'account_reference': 'invalid_reference'  # Invalid member number
        })

        self.assertEqual(response.status_code, 400)  # Expect a bad request
