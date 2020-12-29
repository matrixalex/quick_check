from src.apps.core.models import SafeModel
from django.db import models
from django.utils.translation import gettext_lazy as _


class PupilHomework(SafeModel):
    WAIT = 0
    UPLOADED_NO_ANSWER = 1
    UPLOADED_HAS_ANSWER = 2

    STATUS_CHOICES = (
        (WAIT, _('Ожидает выполнения')),
        (UPLOADED_NO_ANSWER, _('Ожидает обработки сервером')),
        (UPLOADED_HAS_ANSWER, _('Есть ответ'))
    )
    """Модель ответа на домашнее задание, загруженный учеником"""
    pupil = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='pupil_homework_pupil',
                              verbose_name=_('Ученик'))

    homework_exercise = models.ForeignKey('homework.Homework', on_delete=models.CASCADE,
                                          related_name='pupil_homework_exercise',
                                          verbose_name=_('Домашняя работа'))

    pupilhomework_document = models.ForeignKey('core.Document', on_delete=models.CASCADE,
                                               related_name='pupilhomework_document',
                                               verbose_name=_('Файл домашней работы'),
                                               blank=True, null=True)

    mark = models.IntegerField(default=None, verbose_name=_('Оценка за домашнее задание'),
                               null=True, blank=True)

    status = models.IntegerField(default=WAIT, choices=STATUS_CHOICES, verbose_name=_('Статус'))

    class Meta:
        db_table = 'pupil_homeworks'
        verbose_name_plural = _('Домашние работы учеников')
        verbose_name = _('Домашняя работа ученика')

    def __str__(self):
        return 'Домашняя работа {} ученика {}'.format(self.homework_exercise, self.pupil)
