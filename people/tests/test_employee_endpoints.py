from django.utils import timezone
import pytest
from org.tests.factories import DepartmentFactory, UserFactory
from people.tests.factories import EmployeeFactory

pytestmark = pytest.mark.django_db

class TestEmployee:
    endpoint = '/api/people/employees/'

    def test_list_employee(self, api_client):
        user = UserFactory()
        EmployeeFactory.create_batch(
                             3, 
                             author=user
                            )
        client = api_client()
        client.force_authenticate(user=user)
        response = client.get(self.endpoint)
        assert response.status_code == 200
        assert len(response.json()['results']) == 3

    def test_retrieve_employee(self, api_client):
        user = UserFactory()
        employee = EmployeeFactory(author=user)
        url = f"{self.endpoint}{employee.id}/"
        client = api_client()
        client.force_authenticate(user=user)
        response = client.get(url)
        assert response.status_code == 200
        assert response.json()['first_name'] == employee.first_name


    def test_create_employee(self, api_client):
        user = UserFactory()
        department = DepartmentFactory()
        employee_json = {
            'first_name':"Joan",
            'last_name':'Deon',
            'gender':'Female',
            'department':department.id,
            'marital_status': 'Single',
            'date_joined': str(timezone.now().date()),
            'birth_date': str(timezone.now().date())
        }
        client = api_client()
        client.force_authenticate(user=user)
        response = client.post(self.endpoint, employee_json, format='json')
        assert response.status_code == 201
        assert response.json()['first_name'] == employee_json['first_name']


    def test_update_employee_details(self, api_client):
        user = UserFactory()
        employee = EmployeeFactory(author=user)
        employee_json = {
            'first_name':"Jane",
            'last_name':'Deon',
            'gender':'Female',
            'department': employee.department.id,
            'marital_status':employee.marital_status,
        }
        client = api_client()
        client.force_authenticate(user=user)
        url = f"{self.endpoint}{employee.id}/"
        response = client.put(url, employee_json, format='json')
        assert response.status_code == 200
        assert response.json()['first_name'] == employee_json['first_name']

    def test_delete_employee(self, api_client):
        user = UserFactory()
        employee = EmployeeFactory(author=user)
        client = api_client()
        client.force_authenticate(user=user)
        url = f"{self.endpoint}{employee.id}/"
        response = client.delete(url)
        assert response.status_code == 204

        