from django.urls import path
from people.views import employees, documents


urlpatterns = [
    path('employees/', employees.EmployeeView.as_view(), name='employees'),
    path('employees/<int:pk>/', employees.EmployeeDetailView.as_view()),
    path('documents/', documents.DocumentView.as_view(), name='employees'),
    path('documents/<int:pk>/', documents.DocumentDetailView.as_view()),
]