import pytest
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models import User

pytestmark = pytest.mark.django_db

BASE_URL = '/api/auth/'

class TestAuthIntegration:
    def test_login_success(self, client, patient_factory):
        """Тест успешной авторизации"""
        patient = patient_factory()
        user = patient.user
        user.set_password('testpass123')
        user.save()

        data = {
            'username': user.username,
            'password': 'testpass123'
        }

        response = client.post(f'{BASE_URL}login/', data=data)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data
        assert response.data['user']['username'] == user.username
        assert response.data['user']['role'] == 'patient'

    def test_login_failure(self, client, patient_factory):
        """Тест неудачной авторизации"""
        patient = patient_factory()
        user = patient.user
        user.set_password('testpass123')
        user.save()

        data = {
            'username': user.username,
            'password': 'wrongpassword'
        }

        response = client.post(f'{BASE_URL}login/', data=data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'Неверные учетные данные.' in str(response.data)

    def test_token_refresh(self, client, patient_factory):
        """Тест обновления токена"""
        patient = patient_factory()
        user = patient.user
        refresh = RefreshToken.for_user(user)

        data = {
            'refresh': str(refresh)
        }

        response = client.post(f'{BASE_URL}token/refresh/', data=data)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data

    def test_protected_endpoint_access(self, client, patient_factory):
        """Тест доступа к защищенному эндпоинту"""
        patient = patient_factory()
        user = patient.user
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Без токена - доступ запрещен
        response = client.get(f'{BASE_URL}profile/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # С токеном - доступ разрешен
        response = client.get(
            f'{BASE_URL}profile/',
            HTTP_AUTHORIZATION=f'Bearer {access_token}'
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == user.username

    def test_role_based_access(self, client, admin_factory, doctor_factory, patient_factory):
        """Тест ролевого доступа"""
        # Создаем пользователей разных ролей
        admin_user = admin_factory()  # Это уже User объект
        doctor = doctor_factory()     # Это Doctor объект (имеет .user)
        patient = patient_factory()   # Это Patient объект (имеет .user)

        # Получаем токены
        admin_token = str(RefreshToken.for_user(admin_user).access_token)  # Используем admin_user напрямую
        doctor_token = str(RefreshToken.for_user(doctor.user).access_token)
        patient_token = str(RefreshToken.for_user(patient.user).access_token)

        # Проверяем доступ к админскому эндпоинту
        response = client.get(
            f'{BASE_URL}admin-only/',
            HTTP_AUTHORIZATION=f'Bearer {admin_token}'
        )
        assert response.status_code == status.HTTP_200_OK

        response = client.get(
            f'{BASE_URL}admin-only/',
            HTTP_AUTHORIZATION=f'Bearer {doctor_token}'
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

        # Проверяем доступ к докторскому эндпоинту
        response = client.get(
            f'{BASE_URL}doctor-only/',
            HTTP_AUTHORIZATION=f'Bearer {doctor_token}'
        )
        assert response.status_code == status.HTTP_200_OK

        response = client.get(
            f'{BASE_URL}doctor-only/',
            HTTP_AUTHORIZATION=f'Bearer {patient_token}'
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

        # Проверяем доступ к пациентскому эндпоинту
        response = client.get(
            f'{BASE_URL}patient-only/',
            HTTP_AUTHORIZATION=f'Bearer {patient_token}'
        )
        assert response.status_code == status.HTTP_200_OK

        response = client.get(
            f'{BASE_URL}patient-only/',
            HTTP_AUTHORIZATION=f'Bearer {doctor_token}'
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_user_profile_data(self, client, doctor_factory):
        """Тест корректности данных профиля"""
        doctor = doctor_factory(
            first_name='Иван',
            last_name='Петров',
            middle_name='Сергеевич',
            specialization='Кардиолог'
        )
        user = doctor.user
        token = str(RefreshToken.for_user(user).access_token)

        response = client.get(
            f'{BASE_URL}profile/',
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )

        assert response.status_code == status.HTTP_200_OK
        # Проверяем структуру ответа в зависимости от вашей реализации
        if 'user' in response.data:
            # Если данные пользователя вложены в 'user'
            assert response.data['user']['username'] == user.username
            assert response.data['user']['role'] == 'doctor'
        else:
            # Если данные пользователя в корне ответа
            assert response.data['username'] == user.username
            assert response.data['role'] == 'doctor'
        
        # Проверка данных профиля
        if 'profile' in response.data:
            profile_data = response.data['profile']
        else:
            profile_data = response.data
        
        assert profile_data['first_name'] == 'Иван'
        assert profile_data['last_name'] == 'Петров'
        assert profile_data.get('specialization') == 'Кардиолог'