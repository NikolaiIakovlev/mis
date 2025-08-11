from rest_framework import serializers
from .models import Consultation


class ConsultationSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.get_full_name', read_only=True)
    patient_name = serializers.CharField(source='patient.get_full_name', read_only=True)
    clinic_name = serializers.CharField(source='clinic.name', read_only=True)

    class Meta:
        model = Consultation
        fields = [
            'id',
            'start_time',
            'end_time',
            'status',
            'doctor',
            'doctor_name',
            'patient',
            'patient_name',
            'clinic',
            'clinic_name',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
