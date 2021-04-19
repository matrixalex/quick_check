from src.apps.core.models import SafeModel
from django.db import models
from django.utils.translation import gettext_lazy as _


class Criterion(SafeModel):
    KEY_TYPE = 0
    TEXT_TYPE = 1

    TYPE_CHOICES = (
        (KEY_TYPE, _('Тест')),
        (TEXT_TYPE, _('Текст')),
    )

    TEXT_FORMAT = '% выполнения работы на оценку {}'
    MARK_1 = 1
    MARK_2 = 2
    MARK_3 = 3
    MARK_4 = 4
    MARK_5 = 5

    criterion_type = models.IntegerField(default=0, verbose_name=_('Тип критерия'), choices=TYPE_CHOICES)
    name = models.TextField(default='', verbose_name=_('Наименование'))

    part2 = models.IntegerField(default=28, verbose_name=_(TEXT_FORMAT.format(2)))
    part3 = models.IntegerField(default=56, verbose_name=_(TEXT_FORMAT.format(3)))
    part4 = models.IntegerField(default=70, verbose_name=_(TEXT_FORMAT.format(4)))
    part5 = models.IntegerField(default=85, verbose_name=_(TEXT_FORMAT.format(5)))

    max_mistake_count = models.PositiveIntegerField(default=10, verbose_name=_('Допустимое кол-во ошибок'))
    default = models.BooleanField(default=False, editable=False)

    class Meta:
        db_table = 'criterion'
        verbose_name_plural = _('Критерии')
        verbose_name = _('Критерий')

    def __str__(self):
        return 'Критерий {}'.format(self.name)

    def get_mark(self, complete_percent: int):
        assert 0 <= complete_percent <= 100
        if self.criterion_type == self.TEXT_TYPE:
            complete_percent = self.max_mistake_count - complete_percent
            if complete_percent < 0:
                complete_percent = 0
            complete_percent = complete_percent / self.max_mistake_count
        if complete_percent >= self.part5:
            return self.MARK_5
        elif complete_percent >= self.part4:
            return self.MARK_4
        elif complete_percent >= self.part3:
            return self.MARK_3
        elif complete_percent >= self.part2:
            return self.MARK_2
        return self.MARK_2

    @classmethod
    def check_default_criterion(cls):
        print('check_default_criterion')
        if not cls.objects.filter(default=True).exists():
            print('creating default criterion')
            cls.objects.create(name='Обычный (100 баллов)', default=True, criterion_type=cls.KEY_TYPE)
            cls.objects.create(name='Обычный текст (100 баллов)', default=True, criterion_type=cls.TEXT_TYPE)
