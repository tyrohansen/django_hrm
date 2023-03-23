from django.contrib.auth import get_user_model
from django.http import Http404
from org.models import Department
from people.models import Employee, LeaveRequest, Document

User = get_user_model()

def create_employee(
        first_name:str,
        last_name:str,
        gender:str,
        department:Department,
        job_title:str,
        section:str,
        id_no:str,
        nin:str,
        date_joined:str,
        marital_status:str,
        birth_place:str,
        residence:str,
        birth_date:str,
        kin_name:str,
        kin_contact:str,
        emergency_contact:str,
        comment:str,
        author:User,
    ) -> Employee:
    employee = Employee.objects.create(
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        department=department,
        job_title=job_title,
        section=section,
        id_no=id_no,
        nin=nin,
        date_joined=date_joined,
        marital_status=marital_status,
        birth_place=birth_place,
        residence=residence,
        birth_date=birth_date,
        kin_name=kin_name,
        kin_contact=kin_contact,
        emergency_contact=emergency_contact,
        comment=comment,
        author=author,
    )
    return employee

def get_employee_by_id(id:int) -> Employee:
    try:
        return Employee.objects.get(pk=id)
    except Employee.DoesNotExist:
        return None
    

def create_document(
        title:str,
        employee:Employee,
        filename:str,
        category:str,
        notes:str,
        author:User
    ) -> Document:
    pass
