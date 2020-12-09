from src.apps.core.models import SafeModel
from django.db import models
from django.utils.translation import gettext_lazy as _


class HomeworkResult(SafeModel):
    parent = models.ForeignKey('homework.Homework', on_delete=models.CASCADE, related_name='homeworkresult_homework',
                                 verbose_name=_('Задание'))

    pupil = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='homeworkresult_pupil',
                              verbose_name=_('Ученик'))

    mark = models.IntegerField(default=0, verbose_name=_('Оценка'))

    class Meta:
        db_table = 'homework_results'
        verbose_name_plural = _('Ответы на домашние задания')
        verbose_name = _('Ответ на домашнее задание')

    def __str__(self):
        return 'Ответ на домашнюю работу {} ученика {}'.format(self.homework, self.pupil)
