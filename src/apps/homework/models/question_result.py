from src.apps.core.models import SafeModel
from django.db import models
from django.utils.translation import gettext_lazy as _


class QuestionResult(SafeModel):
    questionresult_document = models.ForeignKey('core.Document', on_delete=models.CASCADE,
                                                related_name='questionresult_document',
                                                verbose_name=_('Документ'))

    pupil_homework = models.ForeignKey('homework.PupilHomework', on_delete=models.CASCADE,
                                       related_name='questionresult_pupil_homework', verbose_name=_('Домашняя работа'))

    homework_question = models.ForeignKey('homework.Question', on_delete=models.CASCADE,
                                          related_name='questionresult_homework_question', verbose_name=_('Вопрос'))

    pupil = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='questionresult_pupil',
                              verbose_name=_('Ученик'))

    answer = models.TextField(default='Ответ', verbose_name=_('Ответ'))

    is_correct = models.BooleanField(default=False, verbose_name=_('Правильный ответ'))

    class Meta:
        db_table = 'question_results'
        verbose_name_plural = _('Ответы на вопросы учеников')
        verbose_name = _('Ответ на вопрос ученика')

    def __str__(self):
        return str(self.pupil_homework)
