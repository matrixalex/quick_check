from django.db import models
from .safe_model import SafeModel
from django.utils.translation import gettext_lazy as _


class Organization(SafeModel):
    """Модель организации"""
    name = models.TextField(default=_('Организация'), verbose_name=_('Наименование'))

    class Meta:
        db_table = 'organizations'
        verbose_name_plural = _('Организации')
        verbose_name = _('Организация')

    def __str__(self):
        return self.name
