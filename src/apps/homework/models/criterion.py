from src.apps.core.models import SafeModel
from django.db import models
from django.utils.translation import gettext_lazy as _


class Criterion(SafeModel):
    TEXT_FORMAT = '% выполнения работы на оценку {}'
    MARK_1 = 1
    MARK_2 = 2
    MARK_3 = 3
    MARK_4 = 4
    MARK_5 = 5
    name = models.TextField(default='', verbose_name=_('Наименование'))

    part2 = models.IntegerField(default=28, verbose_name=_(TEXT_FORMAT.format(2)))
    part3 = models.IntegerField(default=56, verbose_name=_(TEXT_FORMAT.format(3)))
    part4 = models.IntegerField(default=70, verbose_name=_(TEXT_FORMAT.format(4)))
    part5 = models.IntegerField(default=85, verbose_name=_(TEXT_FORMAT.format(5)))

    class Meta:
        db_table = 'criterion'
        verbose_name_plural = _('Критерии')
        verbose_name = _('Критерий')

    def __str__(self):
        return 'Критерий {}'.format(self.name)

    def get_mark(self, complete_percent: int):
        assert 0 <= complete_percent <= 100
        if complete_percent >= self.part5:
            return self.MARK_5
        elif complete_percent >= self.part4:
            return self.MARK_4
        elif complete_percent >= self.part3:
            return self.MARK_3
        elif complete_percent >= self.part2:
            return self.MARK_2
        return self.MARK_1

    @classmethod
    def check_default_criterion(cls):
        print('check_default_criterion')
        if not cls.objects.exists():
            print('creating default criterion')
            cls.objects.create(name='Обычная (100 баллов)')
