from django.utils import timezone
import pytest
from org.tests.factories import UserFactory
from people.tests.factories import DocumentFactory, EmployeeFactory


pytestmark = pytest.mark.django_db

class TestDocument:
    endpoint = '/api/people/documents/'

    def test_list_document(self, api_client):
        user = UserFactory()
        employee = DocumentFactory.create_batch(
                             3, 
                             author=user
                            )
        client = api_client()
        client.force_authenticate(user=user)
        response = client.get(self.endpoint)
        print(response.content)
        assert response.status_code == 200
        assert len(response.json()) == 3
        
