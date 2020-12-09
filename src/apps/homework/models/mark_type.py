from src.apps.core.models import SafeModel
from django.db import models
from django.utils.translation import gettext_lazy as _


class MarkType(SafeModel):
    name = models.TextField(default=_('Пятибальная'), verbose_name=_('Тип оценки'))

    def __str__(self):
        return self.name
