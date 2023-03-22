from django.db import models
from django.conf import settings

from org.models import Department


class Employee(models.Model):
    MARITAL_STATUS=(
        ('Single','Single'),
        ('Married','Married'),
        ('Divorced','Divorced')
    )
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    gender = models.CharField(max_length=32, choices=(('Male','Male'),('Female','Female')))
    department = models.ForeignKey(Department, related_name='department_employees', on_delete=models.PROTECT)
    job_title = models.CharField(max_length=200, blank=True, default="")
    section = models.CharField(max_length=200, blank=True, default="")
    id_no = models.CharField(max_length=32, blank=True, default="")
    nin = models.CharField(max_length=32, blank=True, default="")
    date_joined = models.DateField(blank=True)
    marital_status = models.CharField(max_length=32, choices=MARITAL_STATUS)
    birth_place = models.CharField(max_length=200, blank=True, default="")
    residence = models.CharField(max_length=200, blank=True, default="")
    birth_date = models.DateField(blank=True)
    kin_name = models.CharField(max_length=200, blank=True, default="")
    kin_contact = models.CharField(max_length=200, blank=True, default="")
    emergency_contact = models.CharField(max_length=200, blank=True, default="")
    comment = models.TextField(blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_employees', on_delete=models.PROTECT)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)



class Document(models.Model):
    CATEGORIES =(
        ('Personal','Personal'),
        ('Education','Education'),
        ('HR','HR')
    )
    title  = models.CharField(max_length=200)
    employee = models.ForeignKey(Employee, related_name='employee_documents', on_delete=models.CASCADE)
    filename = models.FileField(upload_to='uploads/%Y/%m/%d/')
    category = models.CharField(max_length=32, choices=CATEGORIES)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_employee_documents', on_delete=models.PROTECT)
    notes = models.TextField(blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)


class LeaveRequest(models.Model):
    STATUSES =(
        ('Pending','Pending'),
        ('Approved','Approved'),
        ('Denied','Denied')
    )
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    reason = models.CharField(max_length=255)
    status = models.CharField(max_length=32, choices=STATUSES)
    approved = models.DateTimeField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_employee_requests', on_delete=models.PROTECT)
    notes = models.TextField(blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)