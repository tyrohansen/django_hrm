from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from people.models import Document

from people.serializers import DocumentEditSerializer, DocumentSerializer
from people.services import create_document, get_document_by_id

class DocumentView(APIView):
    serializer_class = DocumentSerializer

    def get(self, request, format=None):
        documents = Document.objects.all()
        return Response(DocumentSerializer(documents, many=True).data, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        form = DocumentSerializer(data=request.data)
        if not form.is_valid():
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
        document = create_document(**form.validated_data, author=request.user)
        return Response(DocumentSerializer(document).data, status=status.HTTP_201_CREATED)


class DocumentDetailView(APIView):
    serializer_class = DocumentSerializer

    def get(self, request, pk, format=None):
        document = get_document_by_id(pk)
        return Response(DocumentSerializer(document).data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        document = get_document_by_id(pk)
        if not document:
            return Response({"detail":"No item found!"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = DocumentEditSerializer(document, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_200_OK)
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        document = get_document_by_id(pk)
        if document:
            document.delete()
            return Response({"detail":"Document Deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        
        return Response({"detail":"No item found!"}, status=status.HTTP_404_NOT_FOUND)