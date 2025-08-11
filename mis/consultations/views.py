from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .models import Consultation
from .serializers import ConsultationSerializer



class ConsultationViewSet(viewsets.ModelViewSet):
    serializer_class = ConsultationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['doctor__user__first_name', 'doctor__user__last_name',
                    'patient__user__first_name', 'patient__user__last_name']
    ordering_fields = ['created_at', 'start_time']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = Consultation.objects.all().select_related(
            'doctor', 'doctor__user',
            'patient', 'patient__user',
            'clinic'
        ).only(
            'status', 'created_at', 'start_time',
            'doctor__id', 'doctor__user__first_name', 'doctor__user__last_name',
            'patient__id', 'patient__user__first_name', 'patient__user__last_name',
            'clinic__id', 'clinic__name'
        )
        return queryset

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
        consultation.save(update_fields=['status'])
        return Response(self.get_serializer(consultation).data)

# class ConsultationViewSet(viewsets.ModelViewSet):
#     queryset = Consultation.objects.all().select_related('doctor', 'patient', 'clinic')
#     serializer_class = ConsultationSerializer
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
#     filterset_fields = ['status']
#     search_fields = ['doctor__user__first_name', 'doctor__user__last_name',
#                      'patient__user__first_name', 'patient__user__last_name']
#     ordering_fields = ['created_at', 'start_time']
#     ordering = ['-created_at']

#     @action(detail=True, methods=['patch'], url_path='change-status')
#     def change_status(self, request, pk=None):
#         consultation = self.get_object()
#         new_status = request.data.get('status')

#         if new_status not in dict(Consultation.Status.choices).keys():
#             return Response(
#                 {'error': 'Недопустимый статус.'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         consultation.status = new_status
#         consultation.save()
#         return Response(self.get_serializer(consultation).data)

