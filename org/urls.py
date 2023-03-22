from django.urls import path
from org.views import DepartmentView, DepartmentDetailView

urlpatterns = [
    path('departments/', DepartmentView.as_view()),
    path('departments/<int:pk>/', DepartmentDetailView.as_view()),
]
