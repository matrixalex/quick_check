from src.apps.core.models import SafeModel
from django.db import models
from django.utils.translation import gettext_lazy as _


class AppealResult(SafeModel):
    parent = models.ForeignKey('homework.HomeworkAppeal', on_delete=models.CASCADE,
                               related_name='appealresult_parent',
                               verbose_name=_('Аппеляция'))

    pupil_homework = models.ForeignKey('homework.PupilHomework', on_delete=models.CASCADE,
                                       related_name='appealresult_pupilhomework',
                                       verbose_name=_('Домашняя работа'))

    text = models.TextField(default='', verbose_name=_('Текст ответа'))

    class Meta:
        db_table = 'appeal_results'
        verbose_name_plural = _('Ответы на аппеляции')
        verbose_name = _('Ответ на аппеляцию')

    def __str__(self):
        return 'Ответ на аппеляцию {}'.format(self.parent)
