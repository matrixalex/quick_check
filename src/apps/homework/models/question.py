from src.apps.core.models import SafeModel
from django.db import models
from django.utils.translation import gettext_lazy as _


class Question(SafeModel):
    """Модель вопроса в домашнем задании"""
    text = models.TextField(default='', verbose_name=_('Вопрос'))
    answer = models.TextField(default='', verbose_name=_('Правильный ответ'))

    question_homework = models.ForeignKey('homework.Homework', on_delete=models.CASCADE,
                                          related_name='question_homework',
                                          verbose_name=_('Домашнее задание'))

    class Meta:
        db_table = 'questions'
        verbose_name_plural = _('Вопросы')
        verbose_name = _('Вопрос')

    def __str__(self):
        return self.text
