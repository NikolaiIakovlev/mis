from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .models import Consultation
from .serializers import ConsultationSerializer


class ConsultationViewSet(viewsets.ModelViewSet):
    queryset = Consultation.objects.all().select_related('doctor', 'patient', 'clinic')
    serializer_class = ConsultationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['doctor__user__first_name', 'doctor__user__last_name',
                     'patient__user__first_name', 'patient__user__last_name']
    ordering_fields = ['created_at', 'start_time']
    ordering = ['-created_at']

    @action(detail=True, methods=['patch'], url_path='change-status')
    def change_status(self, request, pk=None):
        consultation = self.get_object()
        new_status = request.data.get('status')

        if new_status not in dict(Consultation.Status.choices).keys():
            return Response(
                {'error': 'Недопустимый статус.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        consultation.status = new_status
        consultation.save()
        return Response(self.get_serializer(consultation).data)


# from rest_framework import viewsets, filters, status
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from django_filters.rest_framework import DjangoFilterBackend
# from .models import Consultation
# from .serializers import ConsultationSerializer, ConsultationStatusSerializer
# from accounts.permissions import IsDoctorUser, IsPatientUser, IsAdminUser

# class ConsultationViewSet(viewsets.ModelViewSet):
#     queryset = Consultation.objects.all()
#     serializer_class = ConsultationSerializer
#     permission_classes = [IsAuthenticated]
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
#     filterset_fields = ['status', 'doctor', 'patient', 'clinic']
#     search_fields = [
#         'doctor__user__first_name',
#         'doctor__user__last_name',
#         'patient__user__first_name',
#         'patient__user__last_name'
#     ]
#     ordering_fields = ['created_at', 'start_time', 'end_time']
#     ordering = ['-created_at']

#     def get_queryset(self):
#         queryset = super().get_queryset()
        
#         # Фильтрация для врачей - только их консультации
#         if self.request.user.is_doctor():
#             return queryset.filter(doctor=self.request.user.doctor)
        
#         # Фильтрация для пациентов - только их консультации
#         elif self.request.user.is_patient():
#             return queryset.filter(patient=self.request.user.patient)
        
#         # Админ видит все консультации
#         return queryset

#     def get_permissions(self):
#         if self.action in ['create']:
#             return [IsAuthenticated(), IsPatientUser()]
#         elif self.action in ['update', 'partial_update', 'destroy']:
#             return [IsAuthenticated(), IsAdminUser()]
#         return super().get_permissions()

#     @action(detail=True, methods=['patch'])
#     def change_status(self, request, pk=None):
#         consultation = self.get_object()
#         serializer = ConsultationStatusSerializer(
#             consultation, 
#             data=request.data, 
#             partial=True
#         )
        
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)