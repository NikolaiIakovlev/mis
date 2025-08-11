import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from consultations.models import Consultation

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def clinic(db):
    from clinics.models import Clinic
    return Clinic.objects.create(
        name='Test Clinic',
        legal_address='Юридический адрес 1',
        physical_address='Физический адрес 1'
    )

@pytest.fixture
def doctor_user(db, django_user_model):
    user = django_user_model.objects.create_user(username='doctor1', password='pass', role='doctor')
    return user

@pytest.fixture
def patient_user(db, django_user_model):
    user = django_user_model.objects.create_user(username='patient1', password='pass', role='patient')
    return user

@pytest.fixture
def doctor(db, doctor_user, clinic):
    from accounts.models import Doctor
    doc = Doctor.objects.create(user=doctor_user, first_name='Док', last_name='Тор', specialization='Кардиолог')
    doc.clinics.add(clinic)
    return doc

@pytest.fixture
def patient(db, patient_user):
    from accounts.models import Patient
    return Patient.objects.create(user=patient_user, first_name='Паци', last_name='Ент', phonenumber='+123456')

@pytest.fixture
def token(api_client, patient_user):
    response = api_client.post('/api/auth/login/', {
        'username': patient_user.username,
        'password': 'pass'
    })
    assert 'access' in response.data
    return response.data['access']

@pytest.fixture
def auth_client(api_client, token):
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return api_client

@pytest.fixture
def consultation(db, doctor, patient, clinic):
    return Consultation.objects.create(
        start_time="2025-08-20T10:00:00+03:00",
        end_time="2025-08-20T10:30:00+03:00",
        doctor=doctor,
        patient=patient,
        clinic=clinic
    )

@pytest.mark.django_db
def test_create_consultation(auth_client, doctor, patient, clinic):
    url = reverse('consultation-list')
    payload = {
        "start_time": "2025-08-21T14:00:00+03:00",
        "end_time": "2025-08-21T14:30:00+03:00",
        "doctor": doctor.id,
        "patient": patient.id,
        "clinic": clinic.id
    }
    response = auth_client.post(url, payload)
    assert response.status_code == 201
    assert Consultation.objects.count() == 1

@pytest.mark.django_db
def test_get_consultation_list(auth_client, consultation):
    url = reverse('consultation-list')
    response = auth_client.get(url)
    assert response.status_code == 200
    assert response.data['count'] >= 1

@pytest.mark.django_db
def test_filter_by_status(auth_client, consultation):
    consultation.status = 'COMPLETED'
    consultation.save()
    url = reverse('consultation-list') + '?status=COMPLETED'
    response = auth_client.get(url)
    assert response.status_code == 200
    assert response.data['count'] >= 1
    assert response.data['results'][0]['status'] == 'COMPLETED'

@pytest.mark.django_db
def test_update_consultation(auth_client, consultation):
    url = reverse('consultation-detail', args=[consultation.id])
    response = auth_client.patch(url, {"status": "PAID"})
    assert response.status_code == 200
    assert response.data["status"] == "PAID"

@pytest.mark.django_db
def test_delete_consultation(auth_client, consultation):
    url = reverse('consultation-detail', args=[consultation.id])
    response = auth_client.delete(url)
    assert response.status_code == 204
    assert not Consultation.objects.filter(id=consultation.id).exists()

@pytest.mark.django_db
def test_change_status(auth_client, consultation):
    url = reverse('consultation-change-status', args=[consultation.id])
    response = auth_client.patch(url, {"status": "CONFIRMED"})
    assert response.status_code == 200
    assert response.data["status"] == "CONFIRMED"
