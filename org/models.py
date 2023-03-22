from django.db import models
from django.conf import settings

class Department(models.Model):
    name = models.CharField(max_length=200)
    shortname = models.CharField(max_length=8, unique=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_departments', on_delete=models.PROTECT)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
