from django.urls import path
from org.views import DepartmentView

urlpatterns = [
    path('departments/', DepartmentView.as_view()),
]
