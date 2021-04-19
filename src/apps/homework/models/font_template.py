from src.apps.core.models import SafeModel
from django.db import models
from django.utils.translation import gettext_lazy as _


class FontTemplate(SafeModel):
    NUMERIC = 0
    LATIN = 1
    CYRILLIC = 2

    FONT_TEMPLATE_TYPES = (
        (NUMERIC, _('Цифры')),
        (LATIN, _('Латиница')),
        (NUMERIC, _('Кириллица')),
    )

    TEMPLATE_PATHS = {
        NUMERIC: '/static/images/sample_digit.pdf',
        LATIN: '/static/images/sample_latin.pdf',
        CYRILLIC: '/static/images/sample_rus.pdf',
    }
    template_type = models.IntegerField(default=NUMERIC, choices=FONT_TEMPLATE_TYPES, verbose_name=_('Тип шаблона'))
    hidden_homework = models.ForeignKey(
        'homework.PupilHomework',
        on_delete=models.CASCADE,
        verbose_name=_('Скрытая домашняя работа')
    )

    def __str__(self):
        return str(self.hidden_homework)
