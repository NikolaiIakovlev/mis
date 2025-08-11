from rest_framework import serializers
from .models import Clinic


class ClinicSerializer(serializers.ModelSerializer):
    """Сериализатор для клиник с базовой валидацией"""
    class Meta:
        model = Clinic
        fields = ['id', 'name', 'legal_address', 'physical_address']
        read_only_fields = ['id']
        
    def validate_name(self, value):
        """Проверка уникальности названия клиники"""
        if Clinic.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError("Клиника с таким названием уже существует")
        return value
