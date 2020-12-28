from src.apps.core.models import SafeModel
from django.db import models
from django.utils.translation import gettext_lazy as _


class HomeworkAppeal(SafeModel):
    parent = models.ForeignKey('homework.PupilHomework', on_delete=models.CASCADE,
                               related_name='homeworkappeal_homework',
                               verbose_name=_('Вопрос'))

    text = models.TextField(default='', verbose_name=_('Текст аппеляции'))

    homeworkappeal_document = models.ForeignKey('core.Document', on_delete=models.CASCADE,
                                                related_name='homeworkappeal_document',
                                                verbose_name=_('Документ'))

    class Meta:
        db_table = 'homework_appeals'
        verbose_name_plural = _('Аппеляции')
        verbose_name = _('Аппеляция')

    def __str__(self):
        return 'Аппеляция {} на {}'