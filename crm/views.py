from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import viewsets

from .models import Client
from .serializers import ClientSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'source', 'date_of_creation']
    search_fields = ['first_name', 'last_name', 'email', 'phone', 'comment']
    ordering_fields = ['first_name', 'last_name', 'date_of_creation', 'status']
    ordering = ['date_of_creation']
