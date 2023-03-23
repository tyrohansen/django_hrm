from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from people.models import Document

from people.serializers import DocumentSerializer

class DocumentView(APIView):
    serializer_class = DocumentSerializer

    def get(self, request, format=None):
        documents = Document.objects.all()
        return Response(DocumentSerializer(documents, many=True).data, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        pass


class DocumentDetailView(APIView):
    serializer_class = DocumentSerializer

    def get(self, request, pk, format=None):
        pass

    def put(self, request, pk, format=None):
        pass

    def delete(self, request, pk, format=None):
        pass