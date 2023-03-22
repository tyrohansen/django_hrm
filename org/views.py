from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from org.models import Department
from org.serializers import DepartmentSerializer
from org.services import create_department


class DepartmentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        departments = Department.objects.all()
        return Response(DepartmentSerializer(departments, many=True).data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        form = DepartmentSerializer(data=request.data)
        if not form.is_valid():
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
        
        department = create_department(
            name=form.validated_data['name'],
            shortname=form.validated_data['shortname'],
            author=request.user
        )
        return Response(DepartmentSerializer(department).data, status=status.HTTP_201_CREATED)
