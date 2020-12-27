from django.db import models
from src.apps.core.models import SafeModel
from django.utils.translation import gettext_lazy as _


class Homework(SafeModel):
    """Модель домашнего задания, загружаемого учителем"""
    name = models.TextField(default=_('Наименование'), verbose_name=_('Наименование'))
    description = models.TextField(default=_('Описание'), verbose_name=_('Описание'))

    homework_teacher = models.ForeignKey('users.User', on_delete=models.CASCADE,
                                         related_name='homework_exercise_teacher',
                                         verbose_name=_('Учитель'))
    homework_document = models.ForeignKey('core.Document', on_delete=models.CASCADE,
                                          related_name='homework_exercise_document',
                                          verbose_name=_('Файл задания'))

    homework_criterion = models.ForeignKey('homework.Criterion', on_delete=models.CASCADE,
                                           related_name='homework_criterion',
                                           verbose_name=_('Критерий оценки'))

    homework_marktype = models.ForeignKey('homework.MarkType', on_delete=models.CASCADE,
                                          related_name='homework_marktype',
                                          verbose_name=_('Вид оценки'))

    class Meta:
        db_table = 'homeworks'
        verbose_name_plural = _('Домашние работы')
        verbose_name = _('Домашняя работа')

    def __str__(self):
        return '{}: {}'.format(self.homework_teacher, self.name)
