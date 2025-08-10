from django.db import models
from clinics.models import Clinic
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class Person(models.Model):
    first_name = models.CharField("Имя", max_length=100)
    last_name = models.CharField("Фамилия", max_length=100)
    middle_name = models.CharField("Отчество", max_length=100, blank=True, null=True)

    class Meta:
        abstract = True
        ordering = ['last_name', 'first_name']
        indexes = [
            models.Index(fields=['last_name', 'first_name']),
        ]

    @property
    def full_name(self):
        """Полное имя человека."""
        return f"{self.last_name} {self.first_name} {self.middle_name}".strip()

    def __str__(self):
        return self.full_name


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Админ'
        DOCTOR = 'doctor', 'Доктор'
        PATIENT = 'patient', 'Пациент'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.PATIENT,
        verbose_name=_('Роль пользователя')
    )

    @property
    def profile(self):
        """Возвращает связанный профиль (Doctor или Patient)"""
        if hasattr(self, 'doctor'):
            return self.doctor
        elif hasattr(self, 'patient'):
            return self.patient
        return None

    def is_doctor(self):
        return self.role == self.Role.DOCTOR

    def is_patient(self):
        return self.role == self.Role.PATIENT

    def is_admin(self):
        return self.role == self.Role.ADMIN

    def get_full_name(self):
        """Переопределение для использования полного имени из профиля"""
        if self.profile:
            return self.profile.full_name
        return super().get_full_name()


class Doctor(Person):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    specialization = models.CharField("Специализация", max_length=150)
    clinics = models.ManyToManyField(to=Clinic, verbose_name="Клиники")

    class Meta(Person.Meta):
        verbose_name = _('Врач')
        verbose_name_plural = _('Врачи')

    def __str__(self):
        return f"{super().__str__()} - ({self.specialization})"


class Patient(Person):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phonenumber = models.CharField("Телефон", max_length=20)
    email = models.EmailField(blank=True, null=True, verbose_name=_('Email'))

    class Meta(Person.Meta):
        verbose_name = _('Пациент')
        verbose_name_plural = _('Пациенты')