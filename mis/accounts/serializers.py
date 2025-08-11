from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Doctor, Patient


class UserLoginSerializer(serializers.Serializer):
    """Сериализатор для аутентификации пользователя."""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(
                request=self.context.get('request'),
                username=username, password=password
                )
            if not user:
                msg = 'Неверные учетные данные.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Необходимо указать "username" и "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя."""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'first_name', 'last_name']
        read_only_fields = ['id', 'role']


class DoctorProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для профиля доктора."""
    class Meta:
        model = Doctor
        fields = ['first_name', 'last_name', 'middle_name', 'specialization', 'clinics']


class PatientProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для профиля пациента."""
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'middle_name', 'phonenumber', 'email']


class UserWithProfileSerializer(UserSerializer):
    profile = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['profile']

    def get_profile(self, obj):
        if obj.is_doctor() and hasattr(obj, 'doctor'):
            return DoctorProfileSerializer(obj.doctor).data
        elif obj.is_patient() and hasattr(obj, 'patient'):
            return PatientProfileSerializer(obj.patient).data
        return None
