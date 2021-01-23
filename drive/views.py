from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from rest_framework import viewsets
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.generics import ListAPIView
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
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


class IndexView(TemplateView):
    template_name = "index.html"


@api_view(('POST',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def login_view(request, *args, **kwargs):
    context = {}
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        context['object_list'] = Document.objects.filter(owner=user).order_by('-uploaded')
    else:
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
    return render(request, template_name='home.html', context=context)


@login_required
def logout_view(request, *args, **kwargs):
    logout(request)
    return redirect('index')
