from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from people.models import Employee
from people.serializers import EmployeeSerializer
from people.services import create_employee, get_employee_by_id

class EmployeeView(APIView , PageNumberPagination):
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        employees = Employee.objects.all()
        paged_employees = self.paginate_queryset(employees, request, view=self)
        serializer = EmployeeSerializer(paged_employees, many=True, context={'request':request})
        return self.get_paginated_response(serializer.data)
    
    def post(self, request, format=None):
        serializer = EmployeeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        employee = create_employee(**serializer.validated_data, author=request.user)
        return Response(EmployeeSerializer(employee).data, status=status.HTTP_201_CREATED)

class EmployeeDetailView(APIView):
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        employee = get_employee_by_id(pk)
        if employee:
            return Response(EmployeeSerializer(employee).data, status=status.HTTP_200_OK)
        return Response({"detail":"Employee not found!"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk, format=None):
        employee = get_employee_by_id(pk)
        serializer = EmployeeSerializer(employee, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        employee = get_employee_by_id(pk)
        employee.delete()
        return Response({"message":"Item deleted successsfully"}, status=status.HTTP_204_NO_CONTENT)