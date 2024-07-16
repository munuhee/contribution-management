import random
import string
import pytest
from members.models import Member
from transactions.models import Transaction, UnmatchedTransactions


@pytest.fixture
def create_member():
    return Member.objects.create(
        first_name='John',
        last_name='Doe',
        phone_number='0712345678',
        member_number='M12345',
        national_id_number='12345678',
        account_balance=1000.00
    )


@pytest.mark.django_db
class TestTransactionModel:

    def test_transaction_creation(self, create_member):
        transaction = Transaction.objects.create(
            member=create_member,
            amount=500.00
        )
        assert transaction.member == create_member
        assert transaction.amount == 500.00
        assert transaction.reference.startswith("MSBK")

    def test_transaction_str(self, create_member):
        transaction = Transaction.objects.create(
            member=create_member,
            amount=500.00
        )
        assert str(transaction) == (
            f"{transaction.reference} - {transaction.amount}"
        )

    def test_generate_reference(self):
        random_suffix = ''.join(
            random.choices(string.ascii_uppercase + string.digits, k=6)
        )
        expected_reference = f"MSBK{random_suffix}"
        transaction = Transaction()
        reference = transaction.generate_reference()
        assert reference.startswith("MSBK")
        assert len(reference) == len(expected_reference)


@pytest.mark.django_db
class TestUnmatchedTransactionsModel:

    def test_unmatched_transaction_creation(self):
        unmatched_transaction = UnmatchedTransactions.objects.create(
            amount=300.00
        )
        assert unmatched_transaction.amount == 300.00
        assert unmatched_transaction.reference.startswith("UT")

    def test_unmatched_transaction_str(self):
        unmatched_transaction = UnmatchedTransactions.objects.create(
            amount=300.00
        )
        assert str(unmatched_transaction) == (
            f"{unmatched_transaction.reference}"
            f"- {unmatched_transaction.amount}"
        )

    def test_generate_reference(self):
        random_suffix = ''.join(
            random.choices(string.ascii_uppercase + string.digits, k=6)
        )
        expected_reference = f"UT{random_suffix}"
        unmatched_transaction = UnmatchedTransactions()
        reference = unmatched_transaction.generate_reference()
        assert reference.startswith("UT")
        assert len(reference) == len(expected_reference)
