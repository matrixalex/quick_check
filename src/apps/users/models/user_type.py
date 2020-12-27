from django.db import models
from src.apps.core.models import SafeModel
from django.utils.translation import gettext_lazy as _

SYSTEM_ADMIN = 1
ADMIN = 2
TEACHER = 3
PUPIL = 4

DEFAULT_USER_TYPE_CHOICES = {
    SYSTEM_ADMIN: _('Администратор системы'),
    ADMIN: _('Администратор учебного заведения'),
    TEACHER: _('Учитель'),
    PUPIL: _('Ученик')
}

SUPERIOR_USER_TYPES = {
    SYSTEM_ADMIN: SYSTEM_ADMIN,
    ADMIN: SYSTEM_ADMIN,
    TEACHER: ADMIN,
    PUPIL: TEACHER
}


class UserTypeException(Exception):
    def __init__(self, err_msg):
        super(UserTypeException, self).__init__(err_msg)


class UserType(SafeModel):
    """Модель типа учетной записи"""

    name = models.TextField(default=_('Наименование'), verbose_name=_('Наименование'))

    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='user_type_parent',
                               verbose_name=_('Вышестоящий пользователь'), blank=True, null=True)

    class Meta:
        db_table = 'user_types'
        verbose_name_plural = _('Типы учетных записей')
        verbose_name = _('Тип учетной записи')

    def __str__(self):
        return self.name

    @classmethod
    def choices(cls):
        return [(user_type.id, user_type.name) for user_type in cls.objects.all()]

    @classmethod
    def check_user_type(cls, user_type):
        try:
            cls.objects.get(pk=user_type)
            return True
        except UserType.DoesNotExist:
            return False

    @classmethod
    def get_user_type_str(cls, user_type):
        return cls.objects.get(pk=user_type).name

    def get_superior_user_type(self):
        return self.parent or self

    def safe_delete(self):
        if self.id in DEFAULT_USER_TYPE_CHOICES:
            raise UserTypeException('Невозможно удалить тип учетной записи {}'.format(self.name))
        children = self.objects.filter(parent=self)
        for child in children:
            child.safe_delete()
        super(UserType, self).safe_delete()

    @classmethod
    def check_and_create_user_types(cls):
        """Метод проверки существования дефолтных типов учетных записей и их создание при необходимости"""
        print('check_and_create_user_types')
        user_type_ids = list(DEFAULT_USER_TYPE_CHOICES.keys())
        for id in user_type_ids:
            try:
                user_type = cls.objects.get(pk=id)
                check = True
                if user_type.name != DEFAULT_USER_TYPE_CHOICES[id]:
                    user_type.name = DEFAULT_USER_TYPE_CHOICES[id]
                    check = False
                if not user_type.parent or user_type.parent.id != SUPERIOR_USER_TYPES[id]:
                    user_type.parent = cls.objects.get(pk=SUPERIOR_USER_TYPES[id])
                    check = False
                if not check:
                    user_type.save()
            except cls.DoesNotExist:
                print('UserType "{}" DoesNotExist!'.format(DEFAULT_USER_TYPE_CHOICES[id]))
                user_type = cls.objects.create(name=DEFAULT_USER_TYPE_CHOICES[id])
                if id == SYSTEM_ADMIN:
                    user_type.parent = user_type
                else:
                    user_type.parent = cls.objects.get(pk=SUPERIOR_USER_TYPES[id])
                user_type.save()
