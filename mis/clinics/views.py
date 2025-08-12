from rest_framework import viewsets, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import Clinic
from .serializers import ClinicSerializer


class ClinicViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для работы с клиниками.
    Функции:
        get_queryset - получение клиник - get_object
        create - создание клиники
        update - обновление клиники
        partial_update - частичное обновление клиники
        destroy - удаление клиники
    """
    serializer_class = ClinicSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    search_fields = ['name', 'legal_address', 'physical_address']
    ordering_fields = ['name']
    ordering = ['name']

    def get_queryset(self):
        queryset = Clinic.objects.all().only(
            'id', 'name', 'legal_address', 'physical_address'
        )
        return queryset

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return super().get_permissions()
    
