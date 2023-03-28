import pytest

from org.tests.factories import UserFactory
from people.tests.factories import EmployeeFactory

pytestmark = pytest.mark.django_db

class TestEmployee:
    endpoint = '/api/people/employees/'
    def test_list_employee(self, api_client):
        user = UserFactory()
        employees = EmployeeFactory.create_batch(
                             3, 
                             author=user
                            )
        client = api_client()
        client.force_authenticate(user=user)
        response = client.get(self.endpoint)
        assert response.status_code == 200
        