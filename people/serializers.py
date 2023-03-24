from rest_framework import serializers

from people.models import Document, Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
        read_only_fields = ('author','fullname')


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'
        read_only_fields = ('author',)

class DocumentEditSerializer(serializers.ModelSerializer):
    filename = serializers.FileField(required=False, max_length=None, allow_empty_file=True, use_url=True)
    class Meta:
        model = Document
        fields = '__all__'
        read_only_fields = ('author',)