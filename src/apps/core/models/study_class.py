from django.db import models
from .safe_model import SafeModel
from django.utils.translation import gettext_lazy as _


def teacher_validator(*args, **kwargs):
    print(args, kwargs)
    return True


class StudyClass(SafeModel):
    """Модель класса"""
    name = models.TextField(default=_('Организация'), verbose_name=_('Наименование'))

    org = models.ForeignKey('core.Organization', on_delete=models.CASCADE, related_name='study_class_org',
                            verbose_name=_('Организация'))
    teachers = models.ManyToManyField('users.User', related_name='study_class_teachers', validators=[teacher_validator],
                                      verbose_name=_('Учителя'), null=True, blank=True)

    class Meta:
        db_table = 'study_classes'
        verbose_name_plural = _('Классы')
        verbose_name = _('Класс')
        ordering = ['org']

    def __str__(self):
        return '{}: {}'.format(self.name, self.org)
