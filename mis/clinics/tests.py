from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Clinic


class ClinicAPITests(APITestCase):
    def setUp(self):
        self.clinic = Clinic.objects.create(
            name="Тестовая клиника",
            legal_address="Тестовый юридический адрес",
            physical_address="Тестовый физический адрес"
        )
        
    def test_get_clinics_list(self):
        url = reverse('clinic-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        
    def test_get_clinic_detail(self):
        url = reverse('clinic-detail', args=[self.clinic.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Тестовая клиника")