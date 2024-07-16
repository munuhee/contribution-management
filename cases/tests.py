import pytest
from django.urls import reverse
from django.utils import timezone
from .models import Case


@pytest.mark.django_db
class TestCaseModel:

    def test_case_creation(self):
        case = Case.objects.create(
            case_number='C001',
            amount=100.00,
            description='Test case'
        )
        assert case.case_number == 'C001'
        assert case.amount == 100.00
        assert case.description == 'Test case'
        assert case.deadline > timezone.now()

    def test_case_str(self):
        case = Case(
            case_number='C002',
            amount=150.00,
            description='Another case'
        )
        assert str(case) == 'C002'


@pytest.mark.django_db
class TestCaseViews:

    @pytest.fixture
    def create_case(self):
        return Case.objects.create(
            case_number='C003',
            amount=200.00,
            description='Case to be updated'
        )

    def test_list_cases(self, client):
        response = client.get(reverse('list_cases'))
        assert response.status_code == 200
        assert 'cases' in response.context

    def test_add_case(self, client):
        response = client.post(reverse('add_case'), {
            'case_number': 'C004',
            'amount': 250.00,
            'description': 'Newly added case'
        })
        assert response.status_code == 302
        assert Case.objects.filter(case_number='C004').exists()

    def test_update_case(self, client, create_case):
        response = client.post(reverse('update_case', args=[create_case.id]), {
            'case_number': 'C003_updated',
            'amount': 300.00,
            'description': 'Updated case description'
        })
        assert response.status_code == 302
        updated_case = Case.objects.get(id=create_case.id)
        assert updated_case.case_number == 'C003_updated'
        assert updated_case.amount == 300.00

    def test_delete_case(self, client, create_case):
        response = client.post(reverse('delete_case', args=[create_case.id]))
        assert response.status_code == 302
        assert not Case.objects.filter(id=create_case.id).exists()
