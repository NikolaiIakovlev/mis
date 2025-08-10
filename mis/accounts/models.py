# from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _


class Doctor(models.Model):
    first_name = models.CharField("Имя", max_length=100)
    last_name = models.CharField("Фамилия", max_length=100)
    middle_name = models.CharField("Отчество", max_length=100, blank=True, null=True)
    specialization = models.CharField("Специализация", max_length=150)

    class Meta:
        verbose_name = _('Врач')
        verbose_name_plural = _('Врачи')
        ordering = ['last_name', 'first_name']
        indexes = [
            models.Index(fields=['last_name', 'first_name']),
        ]

    @property
    def full_name(self):
        """Полное имя врача."""
        return f"{self.last_name} {self.first_name} {self.middle_name}".strip()

    def __str__(self):
        return f"{self.full_name}"



class Patient(models.Model):
    first_name = models.CharField("Имя", max_length=100)
    last_name = models.CharField("Фамилия", max_length=100)
    middle_name = models.CharField("Отчество", max_length=100, blank=True, null=True)
    phonenumber = models.CharField("Телефон", max_length=20)
    email = models.EmailField(
        blank=True,
        null=True,
        verbose_name=_('Email')
    )

    class Meta:
        verbose_name = _('Пациент')
        verbose_name_plural = _('Пациенты')
        ordering = ['last_name', 'first_name']
        indexes = [
            models.Index(fields=['last_name', 'first_name']),
        ]

    @property
    def full_name(self):
        """Полное имя пациента."""
        return f"{self.last_name} {self.first_name} {self.middle_name}".strip()

    def __str__(self):
        return f"{self.full_name}"
    





# # class User(AbstractUser):
# #     """Модель пользователя с расширенными полями."""
# #     class Role(models.TextChoices):
# #         ADMIN = 'ADMIN', _('Администратор')
# #         DOCTOR = 'DOCTOR', _('Врач')
# #         PATIENT = 'PATIENT', _('Пациент')
    
# #     role = models.CharField(
# #         max_length=10,
# #         choices=Role.choices,
# #         verbose_name=_('Роль')
# #     )
# #     phone = models.CharField(
# #         max_length=20,
# #         blank=True,
# #         null=True,
# #         verbose_name=_('Телефон')
# #     )
# #     email = models.EmailField(
# #         blank=True,
# #         null=True,
# #         verbose_name=_('Email')
# #     )
# #     specialization = models.CharField(
# #         max_length=100,
# #         blank=True,
# #         null=True,
# #         verbose_name=_('Специализация')
# #     )
# #     created_at = models.DateTimeField(
# #         auto_now_add=True,
# #         verbose_name=_('Дата создания')
# #     )
# #     updated_at = models.DateTimeField(
# #         auto_now=True,
# #         verbose_name=_('Дата обновления')
# #     )
    
# #     # Для разрешения конфликта с auth.User
# #     groups = models.ManyToManyField(
# #         Group,
# #         verbose_name=_('Группы'),
# #         blank=True,
# #         related_name='custom_user_set',
# #         related_query_name='user'
# #     )
# #     user_permissions = models.ManyToManyField(
# #         Permission,
# #         verbose_name=_('Права пользователя'),
# #         blank=True,
# #         related_name='custom_user_set',
# #         related_query_name='user'
# #     )

# #     @property
# #     def full_name(self):
# #         """Полное имя пользователя."""
# #         return f"{self.last_name} {self.first_name}".strip()

# #     def __str__(self):
# #         return f"{self.full_name}"

# #     class Meta:
# #         verbose_name = _('Пользователь')
# #         verbose_name_plural = _('Пользователи')
# #         ordering = ['last_name', 'first_name']
# #         indexes = [
# #             models.Index(fields=['role']),
# #             models.Index(fields=['last_name', 'first_name']),
# #         ]


# class DoctorClinic(models.Model):
#     """Связь врача с клиникой."""
#     doctor = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='clinics',
#         verbose_name=_('Врач')
#     )
#     clinic = models.ForeignKey(
#         'clinics.Clinic',
#         on_delete=models.CASCADE,
#         verbose_name=_('Клиника')
#     )
    
#     def __str__(self):
#         return f"{self.doctor} → {self.clinic}"

#     class Meta:
#         verbose_name = _('Связь врач-клиника')
#         verbose_name_plural = _('Связи врачи-клиники')
#         unique_together = ('doctor', 'clinic')
#         indexes = [
#             models.Index(fields=['doctor']),
#             models.Index(fields=['clinic']),
#         ]