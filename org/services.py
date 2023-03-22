from org.models import Department
from django.contrib.auth import get_user_model


User = get_user_model()

def create_department(name:str, shortname:str, author:User) -> Department:
    department = Department.objects.create(
        name=name,
        shortname=shortname,
        author=author
    )
    return department