import pytest
from django.urls import reverse
from .models import Member


@pytest.mark.django_db
class TestMemberModel:

    def test_member_creation(self):
        member = Member.objects.create(
            first_name='John',
            last_name='Doe',
            phone_number='1234567890',
            member_number='M001',
            national_id_number='NID123456',
            account_balance=1000.00
        )
        assert member.first_name == 'John'
        assert member.last_name == 'Doe'
        assert member.member_number == 'M001'
        assert member.account_balance == 1000.00

    def test_member_str(self):
        member = Member(first_name='Jane', last_name='Smith')
        assert str(member) == 'Jane Smith'


@pytest.mark.django_db
class TestMemberViews:

    @pytest.fixture
    def create_member(self):
        return Member.objects.create(
            first_name='Alice',
            last_name='Johnson',
            phone_number='0987654321',
            member_number='M002',
            national_id_number='NID654321',
            account_balance=500.00
        )

    def test_list_members(self, client):
        response = client.get(reverse('list_members'))
        assert response.status_code == 200
        assert 'members' in response.context

    def test_add_member(self, client):
        response = client.post(reverse('add_member'), {
            'first_name': 'Bob',
            'last_name': 'Brown',
            'phone_number': '1122334455',
            'member_number': 'M003',
            'national_id_number': 'NID789012',
            'account_balance': 1500.00
        })
        assert response.status_code == 302
        assert Member.objects.filter(member_number='M003').exists()

    def test_update_member(self, client, create_member):
        response = client.post(
            reverse('update_member', args=[create_member.id]),
            {
                'first_name': 'Alice Updated',
                'last_name': 'Johnson',
                'phone_number': '0987654321',
                'member_number': 'M002',
                'national_id_number': 'NID654321',
                'account_balance': 600.00
            }
        )
        assert response.status_code == 302
        updated_member = Member.objects.get(id=create_member.id)
        assert updated_member.first_name == 'Alice Updated'
        assert updated_member.account_balance == 600.00

    def test_delete_member(self, client, create_member):
        response = client.post(
            reverse('delete_member', args=[create_member.id])
        )
        assert response.status_code == 302
        assert not Member.objects.filter(id=create_member.id).exists()
