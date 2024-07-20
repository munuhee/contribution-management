import pytest
from .sms_utils import send_sms


@pytest.fixture
def mock_requests_post(mocker):
    return mocker.patch('requests.post')


def test_send_sms_success(mock_requests_post):
    mock_requests_post.return_value.status_code = 200
    mock_requests_post.return_value.json.return_value = {
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
    assert response is not None
    assert response["SMSMessageData"]["Recipients"][0]["status"] == "Success"


def test_send_sms_failure(mock_requests_post):
    mock_requests_post.return_value.status_code = 400  # Simulate an error

    response = send_sms("+254711XXXYYY", "Hello World!")
    assert response is None
