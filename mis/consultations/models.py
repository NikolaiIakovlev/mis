from django.db import models
from django.utils.translation import gettext_lazy as _


class Consultation(models.Model):
    """Модель консультации пациента с врачом."""
    class Status(models.TextChoices):
        CONFIRMED = 'CONFIRMED', _('Подтверждена')
        PENDING = 'PENDING', _('Ожидает')
        STARTED = 'STARTED', _('Начата')
        COMPLETED = 'COMPLETED', _('Завершена')
        PAID = 'PAID', _('Оплачена')
    
    start_time = models.DateTimeField(
        verbose_name=_('Время начала')
    )
    end_time = models.DateTimeField(
        verbose_name=_('Время окончания')
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name=_('Статус')
    )
    doctor = models.ForeignKey(
        'accounts.Doctor',
        on_delete=models.PROTECT,
        related_name='doctor_consultations',
        verbose_name=_('Врач')
    )
    patient = models.ForeignKey(
        'accounts.Patient',
        on_delete=models.PROTECT,
        related_name='patient_consultations',
        verbose_name=_('Пациент')
    )
    clinic = models.ForeignKey(
        'clinics.Clinic',
        on_delete=models.PROTECT,
        verbose_name=_('Клиника')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата создания')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Дата обновления')
    )

    def __str__(self):
        return f"{self.doctor} → {self.patient}"

    class Meta:
        verbose_name = _('Консультация')
        verbose_name_plural = _('Консультации')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['start_time', 'end_time']),
            models.Index(fields=['doctor']),
            models.Index(fields=['patient']),
            models.Index(fields=['clinic']),
        ]