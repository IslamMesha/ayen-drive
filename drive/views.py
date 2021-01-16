from django.views.generic.list import ListView
from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from drive.models import Document
from drive.serializers import DocumentSerializer
from drive.utils import get_docs_list


class DocumentViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing documents.
    """
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly, ]


class DocumentSearch(ListAPIView):
    queryset = Document.objects.all()

    def list(self, request, *args, **kwargs):
        docs = get_docs_list(request, self.get_queryset())
        return Response(data=DocumentSerializer(docs, many=True).data)


class HomePageView(ListView):
    paginate_by = 3
    model = Document
    template_name = 'home.html'
    context_object_name = 'docs'
    queryset = Document.objects.order_by('-uploaded')
