from org.models import Department
import factory
from django.contrib.auth import get_user_model
from faker import Factory

User = get_user_model()
faker = Factory.create()
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    username = factory.Sequence(lambda n: 'User%d' % n)
    email = faker.email()
    password = faker.password()


class DepartmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Department 

    name = factory.Sequence(lambda n: 'Department %d' % n)
    shortname=factory.Sequence(lambda n: 'dpt%d' % n)
    author = factory.SubFactory(UserFactory)