from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Consultation, User, Doctor, Patient, Clinic

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        return token

class ClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = ['id', 'name', 'address']

class DoctorSerializer(serializers.ModelSerializer):
    clinics = ClinicSerializer(many=True, read_only=True)
    
    class Meta:
        model = Doctor
        fields = ['id', 'user', 'specialization', 'clinics']

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'user', 'phone']

class ConsultationSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only=True)
    patient = PatientSerializer(read_only=True)
    clinic = ClinicSerializer(read_only=True)
    
    class Meta:
        model = Consultation
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class ConsultationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation
        fields = ['doctor', 'clinic', 'date_time', 'notes']

class ConsultationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation
        fields = ['status']