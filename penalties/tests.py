import pytest
from django.urls import reverse
from .models import Penalty


@pytest.mark.django_db
class TestPenaltyModel:

    def test_penalty_creation(self, create_member, create_case):
        penalty = Penalty.objects.create(
            member=create_member,
            case=create_case,
            amount=50.00
        )
        assert penalty.member == create_member
        assert penalty.case == create_case
        assert penalty.amount == 50.00
        assert penalty.is_paid is False

    def test_penalty_str(self, create_member, create_case):
        penalty = Penalty(member=create_member, case=create_case)
        assert str(penalty) == f"Penalty for {create_member} on {create_case}"


@pytest.mark.django_db
class TestPenaltyViews:

    @pytest.fixture
    def create_penalty(self, create_member, create_case):
        return Penalty.objects.create(
            member=create_member,
            case=create_case,
            amount=50.00
        )

    def test_list_penalties(self, client):
        response = client.get(reverse('list_penalties'))
        assert response.status_code == 200
        assert 'penalties' in response.context

    def test_add_penalty(self, client, create_member, create_case):
        response = client.post(reverse('add_penalty'), {
            'member': create_member.id,
            'case': create_case.id,
            'amount': 100.00
        })
        assert response.status_code == 302
        assert Penalty.objects.filter(amount=100.00).exists()

    def test_update_penalty(self, client, create_penalty):
        response = client.post(
            reverse('update_penalty', args=[create_penalty.id]),
            {
                'member': create_penalty.member.id,
                'case': create_penalty.case.id,
                'amount': 75.00
            }
        )
        assert response.status_code == 302
        updated_penalty = Penalty.objects.get(id=create_penalty.id)
        assert updated_penalty.amount == 75.00

    def test_delete_penalty(self, client, create_penalty):
        response = client.post(
            reverse('delete_penalty', args=[create_penalty.id])
        )
        assert response.status_code == 302
        assert not Penalty.objects.filter(id=create_penalty.id).exists()
