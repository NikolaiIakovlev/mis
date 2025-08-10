from django.db import models
from django.utils.translation import gettext_lazy as _


class Clinic(models.Model):
    """Модель медицинской клиники."""
    name = models.CharField(
        max_length=255,
        verbose_name=_('Название')
    )
    legal_address = models.TextField(
        verbose_name=_('Юридический адрес')
    )
    physical_address = models.TextField(
        verbose_name=_('Физический адрес')
    )
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Клиника')
        verbose_name_plural = _('Клиники')
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]