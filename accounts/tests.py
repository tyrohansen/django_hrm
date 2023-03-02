from django.urls import reverse
import pytest
from accounts.models import User
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
   from rest_framework.test import APIClient
   return APIClient()

@pytest.mark.django_db
def test_user_create():
  User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
  assert User.objects.count() == 1

@pytest.mark.django_db
def test_unauthorized_request(api_client):
   url = reverse('user-list')
   response = api_client.get(url)
   assert response.status_code == 403