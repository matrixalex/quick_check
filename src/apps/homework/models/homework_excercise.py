from django.db import models
from src.apps.core.models import SafeModel
from django.utils.translation import gettext_lazy as _


class HomeworkExercise(SafeModel):
    """Модель домашнего задания, загружаемого учителем"""
    name = models.TextField(default=_('Наименование'), verbose_name=_('Наименование'))
    teacher = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='homework_exercise_teacher',
                                verbose_name=_('Учитель'))
    document = models.ForeignKey('core.Document', on_delete=models.CASCADE, related_name='homework_exercise_document',
                                 verbose_name=_('Файл задания'))

    criterion = models.ForeignKey()

    