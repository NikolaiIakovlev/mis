from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Модель пользователя с расширенными полями."""
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', _('Администратор')
        DOCTOR = 'DOCTOR', _('Врач')
        PATIENT = 'PATIENT', _('Пациент')
    
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        verbose_name=_('Роль')
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name=_('Телефон')
    )
    specialization = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_('Специализация')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата создания')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Дата обновления')
    )
    
    # Для разрешения конфликта с auth.User
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('Группы'),
        blank=True,
        related_name='custom_user_set',
        related_query_name='user'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('Права пользователя'),
        blank=True,
        related_name='custom_user_set',
        related_query_name='user'
    )

    @property
    def full_name(self):
        """Полное имя пользователя."""
        return f"{self.last_name} {self.first_name}".strip()

    def __str__(self):
        return f"{self.full_name}"

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')
        ordering = ['last_name', 'first_name']
        indexes = [
            models.Index(fields=['role']),
            models.Index(fields=['last_name', 'first_name']),
        ]


class DoctorClinic(models.Model):
    """Связь врача с клиникой."""
    doctor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='clinics',
        verbose_name=_('Врач')
    )
    clinic = models.ForeignKey(
        'clinics.Clinic',
        on_delete=models.CASCADE,
        verbose_name=_('Клиника')
    )
    
    def __str__(self):
        return f"{self.doctor} → {self.clinic}"

    class Meta:
        verbose_name = _('Связь врач-клиника')
        verbose_name_plural = _('Связи врачи-клиники')
        unique_together = ('doctor', 'clinic')
        indexes = [
            models.Index(fields=['doctor']),
            models.Index(fields=['clinic']),
        ]