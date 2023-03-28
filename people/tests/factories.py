import factory
from org.tests.factories import DepartmentFactory, UserFactory
from django.utils import timezone
from people.models import Employee

class EmployeeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Employee
    first_name = 'John'
    last_name = 'Doe'
    gender = 'Male'
    department=factory.SubFactory(DepartmentFactory)
    marital_status='Married'
    author = factory.SubFactory(UserFactory)
    date_joined = timezone.now()
    birth_date = timezone.now()