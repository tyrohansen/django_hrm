import json
import pytest
from .factories import DepartmentFactory, UserFactory

pytestmark = pytest.mark.django_db

class TestDepartment:
    endpoint = "/api/org/departments/"
    def setUp(self):
        self.user = UserFactory()

    def test_list_departments(self, api_client):
        user = UserFactory()
        departments = DepartmentFactory.create_batch(
                             3, 
                             author=user
                            )
        client = api_client()
        client.force_authenticate(user=user)
        response = client.get(
            self.endpoint
        )
        assert response.status_code == 200
        assert len(response.json()) == 3

    def test_retrieve_department(self, api_client):
        user = UserFactory()
        department = DepartmentFactory(author=user)
        url = f'{self.endpoint}{department.id}/'
        client = api_client()
        client.force_authenticate(user=user)
        response = client.get(url)
        assert response.status_code == 200
        assert response.json()['name'] == department.name

    def test_create_department(self, api_client):
        user = UserFactory()
        department_json = {
            'name': "Department one",
            'shortname': "DPT1"
        }
        client = api_client()
        client.force_authenticate(user=user)
        response = client.post(self.endpoint, department_json, format='json')
        assert response.status_code == 201

    def test_update_department(self, api_client):
        user = UserFactory()
        department = DepartmentFactory(author=user)
        department_updated = {
            'name': 'Update department name',
            'shortname': 'UDPT1'
        }
        url = f'{self.endpoint}{department.id}/'
        client = api_client()
        client.force_authenticate(user=user)
        response = client.put(url, department_updated, format='json')
        assert response.status_code == 200
        assert response.json()['name'] == department_updated['name']

    def test_delete_department(self, api_client):
        user = UserFactory()
        department = DepartmentFactory(author=user)
        url = f'{self.endpoint}{department.id}/'
        client = api_client()
        client.force_authenticate(user=user)
        response = client.delete(url)
        assert response.status_code == 204

    def test_authenticated_list_department(self, api_client):
        user = UserFactory()
        departments = DepartmentFactory.create_batch(
                             3, 
                             author=user
                            )
        client = api_client()
        response = client.get(
            self.endpoint
        )
        assert response.status_code == 403
