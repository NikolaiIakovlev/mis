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

# from rest_framework import serializers
# from .models import Consultation
# from accounts.models import Doctor, Patient  # Импортируем модели
# from clinics.models import Clinic
# from accounts.serializers import DoctorProfileSerializer, PatientProfileSerializer
# from clinics.serializers import ClinicSerializer

# class ConsultationSerializer(serializers.ModelSerializer):
#     doctor = DoctorProfileSerializer(read_only=True)
#     patient = PatientProfileSerializer(read_only=True)
#     clinic = ClinicSerializer(read_only=True)
    
#     # Используем PrimaryKeyRelatedField с явным указанием queryset
#     doctor_id = serializers.PrimaryKeyRelatedField(
#         queryset=Doctor.objects.all(), 
#         source='doctor',
#         write_only=True
#     )
#     patient_id = serializers.PrimaryKeyRelatedField(
#         queryset=Patient.objects.all(),
#         source='patient',
#         write_only=True
#     )
#     clinic_id = serializers.PrimaryKeyRelatedField(
#         queryset=Clinic.objects.all(),
#         source='clinic',
#         write_only=True
#     )

#     class Meta:
#         model = Consultation
#         fields = [
#             'id',
#             'start_time',
#             'end_time',
#             'status',
#             'doctor',
#             'patient',
#             'clinic',
#             'doctor_id',
#             'patient_id',
#             'clinic_id',
#             'created_at',
#             'updated_at'
#         ]
#         read_only_fields = ['status', 'created_at', 'updated_at']

# class ConsultationStatusSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Consultation
#         fields = ['status']