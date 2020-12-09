from django.db import models
from src.apps.core.models import SafeModel
from django.utils.translation import gettext_lazy as _


class Homework(SafeModel):
    """Модель домашнего задания, загружаемого учителем"""
    name = models.TextField(default=_('Наименование'), verbose_name=_('Наименование'))
    homework_teacher = models.ForeignKey('users.User', on_delete=models.CASCADE,
                                         related_name='homework_exercise_teacher',
                                         verbose_name=_('Учитель'))
    homework_document = models.ForeignKey('core.Document', on_delete=models.CASCADE,
                                          related_name='homework_exercise_document',
                                          verbose_name=_('Файл задания'))

    homework_criterion = models.ForeignKey('homework.Criterion', on_delete=models.CASCADE,
                                           related_name='homework_criterion',
                                           verbose_name=_('Критерий оценки'))

