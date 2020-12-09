from src.apps.core.models import SafeModel
from django.db import models
from django.utils.translation import gettext_lazy as _


class MarkType(SafeModel):
    name = models.TextField(default=_('Пятибальная'), verbose_name=_('Тип оценки'))

    class Meta:
        db_table = 'mark_types'
        verbose_name_plural = _('Виды оценок')
        verbose_name = _('Вид оценки')

    def __str__(self):
        return self.name
