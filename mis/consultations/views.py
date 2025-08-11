from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Consultation
from .serializers import (
    ConsultationSerializer,
    ConsultationCreateSerializer,
    ConsultationStatusSerializer
)
from .permissions import (
    IsAdmin,
    IsDoctor,
    IsPatient,
    IsDoctorOrAdmin,
    IsPatientOrAdmin
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class ConsultationViewSet(viewsets.ModelViewSet):
    queryset = Consultation.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'clinic']
    search_fields = [
        'doctor__user__last_name', 'doctor__user__first_name',
        'patient__user__last_name', 'patient__user__first_name'
    ]
    ordering_fields = ['date_time', 'created_at']
    ordering = ['-date_time']

    def get_serializer_class(self):
        if self.action == 'create':
            return ConsultationCreateSerializer
        elif self.action == 'change_status':
            return ConsultationStatusSerializer
        return ConsultationSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsPatient]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAdmin]
        elif self.action == 'change_status':
            permission_classes = [IsDoctorOrAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        patient = self.request.user.patient_profile
        serializer.save(patient=patient, status='created')

    @action(detail=True, methods=['patch'])
    def change_status(self, request, pk=None):
        consultation = self.get_object()
        serializer = self.get_serializer(consultation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        if user.role == 'doctor':
            return queryset.filter(doctor__user=user)
        elif user.role == 'patient':
            return queryset.filter(patient__user=user)
        return queryset