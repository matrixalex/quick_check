from src.apps.core.models import SafeModel
from django.db import models
from django.utils.translation import gettext_lazy as _


class PupilHomework(SafeModel):
    """Модель ответа на домашнее задание, загруженный учеником"""
    pupil = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='pupil_homework_pupil',
                              verbose_name=_('Ученик'))

    pupil_homework_document = models.ForeignKey('core.Document', on_delete=models.CASCADE,
                                                related_name='pupil_homework_document',
                                                verbose_name=_('Файл домашней работы'))

    homework_exercise = models.ForeignKey('homework.Homework', on_delete=models.CASCADE,
                                          related_name='pupil_homework_exercise',
                                          verbose_name=_('Файл домашней работы'))

    mark = models.IntegerField(default=2, verbose_name=_('Оценка за домашнее задание'))

    class Meta:
        db_table = 'pupil_homeworks'
        verbose_name_plural = _('Домашние работы учеников')
        verbose_name = _('Домашняя работа ученика')

    def __str__(self):
        return 'Домашняя работа {} ученика {}'.format(self.homework_exercise, self.pupil)
