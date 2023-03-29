import io
from django.utils import timezone
import pytest
from org.tests.factories import UserFactory
from people.tests.factories import DocumentFactory, EmployeeFactory


pytestmark = pytest.mark.django_db

class TestDocument:
    endpoint = '/api/people/documents/'

    def test_list_document(self, api_client):
        user = UserFactory()
        DocumentFactory.create_batch(
                             3, 
                             author=user
                            )
        client = api_client()
        client.force_authenticate(user=user)
        response = client.get(self.endpoint)
        assert response.status_code == 200
        assert len(response.json()) == 3

    def test_retrieve_document(self, api_client):
        user = UserFactory()
        document = DocumentFactory()
        url = f"{self.endpoint}{document.id}/"
        client = api_client()
        client.force_authenticate(user=user)
        response = client.get(url)
        assert response.status_code == 200
        assert response.json()['title'] == document.title


    def test_create_document(self, api_client):
        user = UserFactory()
        employee = EmployeeFactory()
        doc_data ={
            'title':'A Document two',
            'employee':employee.id,
            'category':'Personal',
            'notes': 'These are some notes'
        }
        doc_data['filename'] = (io.BytesIO(b"abcdef"), 'test.jpg')
        client = api_client()
        client.force_authenticate(user=user)
        response = client.post(self.endpoint, data=doc_data, content_type='multipart/form-data')
        print(response.content)
        assert response.status_code == 201
        assert response.json()['title'] == doc_data['title']

    
    def test_delete_document(self, api_client):
        user = UserFactory()
        document = DocumentFactory()
        url = f"{self.endpoint}{document.id}/"
        client = api_client()
        client.force_authenticate(user=user)
        response = client.delete(url)
        assert response.status_code == 204
