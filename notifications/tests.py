from django.test import TestCase
from unittest.mock import patch
from .sms_utils import send_sms


class SmsUtilsTest(TestCase):

    @patch('requests.post')
    def test_send_sms_success(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "SMSMessageData": {
                "Message": "Sent to 1/1 Total Cost: KES 0.8000",
                "Recipients": [{
                    "statusCode": 101,
                    "number": "+254711XXXYYY",
                    "status": "Success",
                    "cost": "KES 0.8000",
                    "messageId": "ATPid_SampleTxnId123"
                }]
            }
        }

        response = send_sms("+254711XXXYYY", "Hello World!")
        self.assertIsNotNone(response)
        self.assertEqual(
            response["SMSMessageData"]["Recipients"][0]["status"], "Success"
        )

    @patch('requests.post')
    def test_send_sms_failure(self, mock_post):
        mock_post.return_value.status_code = 400  # Simulate an error

        response = send_sms("+254711XXXYYY", "Hello World!")
        self.assertIsNone(response)
