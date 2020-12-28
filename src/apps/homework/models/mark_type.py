from src.apps.core.models import SafeModel
from django.db import models
from django.utils.translation import gettext_lazy as _


class MarkType(SafeModel):
    name = models.TextField(default=_('Пятибальная'), verbose_name=_('Тип оценки'))

    default = models.BooleanField(default=False, editable=False)

    class Meta:
        db_table = 'mark_types'
        verbose_name_plural = _('Виды оценок')
        verbose_name = _('Вид оценки')

    def __str__(self):
        return self.name

    @classmethod
    def check_default_marktype(cls):
        print('check_default_marktype')
        if not cls.objects.filter(default=True).exists():
            print('creating default marktype')
            cls.objects.create(name='Патибальная', default=True)
