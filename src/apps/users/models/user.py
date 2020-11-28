from django.contrib.auth.models import AbstractUser, BaseUserManager, Permission
from src.apps.core.models import SafeModel, SafeModelManager, ExtendedModelManager
from django.db import models
from typing import List
from django.utils.translation import gettext_lazy as _
import uuid


class UserType(models.IntegerChoices):
    """
    Класс типов пользователей
    """
    SYSTEM_ADMIN = 0, _('Администратор системы')
    ADMIN = 1, _('Администратор учебного заведения')
    TEACHER = 2, _('Учитель')
    PUPIL = 3, _('Ученик')

    @classmethod
    def check_user_type(cls, user_type):
        return user_type in dict(cls.choices)

    @classmethod
    def get_user_type_str(cls, user_type):
        return dict(cls.choices)[user_type]

    @classmethod
    def get_superior_user_type(cls, user_type):
        if user_type == cls.SYSTEM_ADMIN:
            user_type += 1
        return cls.get_user_type_str(user_type - 1)


class UserManager(SafeModelManager, BaseUserManager):
    """
    Менеджер пользователей
    """
    def create_user(self, email, first_name, last_name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)

        user = self.model(
            email=email,
            username=email,
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, first_name, last_name):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.save(using=self._db)
        user.is_superuser = True
        user.is_staff = True
        user.is_accepted = True
        user.status = UserType.SYSTEM_ADMIN
        user.set_password(password)
        user.save()
        user.user_permissions.set(Permission.objects.all())
        return user

    def not_superusers(self):
        return super(UserManager, self).get_queryset().exclude(is_superuser=True)


class User(SafeModel, AbstractUser):
    """
    Модель пользователя
    """

    RELATED_MODELS = {'users': {'model': 'RegistrationRequest', 'related_field': 'registration_user'}}
    MAX_LENGTH = 100
    first_name = models.CharField(default=_('Имя'), max_length=MAX_LENGTH,
                                  blank=False, null=False, verbose_name=_('Имя'))
    last_name = models.CharField(default=_('Фамилия'), max_length=MAX_LENGTH,
                                 blank=False, null=False, verbose_name=_('Фамилия'))
    middle_name = models.CharField(default='', max_length=MAX_LENGTH,
                                   blank=True, null=False, verbose_name=_('Отчество'))

    phone_number = models.CharField(default='', max_length=12, verbose_name=_('Номер телефона'))

    uuid = models.UUIDField(default=uuid.uuid4(), editable=False)

    email = models.EmailField(unique=True, null=False, max_length=MAX_LENGTH, verbose_name=_('Email пользователя'))

    status = models.IntegerField(default=UserType.PUPIL, choices=UserType.choices, verbose_name=_('Тип учетной записи'))

    is_accepted = models.BooleanField(default=False, verbose_name=_('Пользователь активен'))

    REQUIRED_FIELDS = ['first_name', 'last_name']
    USERNAME_FIELD = 'email'

    objects = UserManager()

    class Meta:
        db_table = u'users'
        verbose_name = u'Пользователь'
        verbose_name_plural = u'Пользователи'
        ordering = ['last_name', 'first_name', 'middle_name']
        permissions = (
            ('Редактирование пользователя', 'user_change'),
            ('Добавление пользователя', 'user_add'),
            ('Удаление пользователя', 'user_delete')
        )

    def __str__(self):
        result = self.last_name + ' ' + self.first_name
        if self.middle_name:
            result += ' ' + self.middle_name
        return result

    def save(self, *args, **kwargs):
        if self.username != self.email:
            self.username = self.email
        super(User, self).save(*args, **kwargs)

    def has_perm(self, perm, obj=None):
        return self.is_superuser or perm in get_user_permissions(self)

    def has_module_perms(self, app_label):
        return self.is_superuser or app_label in get_user_module_permissions(self)

    def accept_registration(self):
        self.is_accepted = True
        self.save()

    def check_site_permission(self):
        return not self.is_deleted and self.is_accepted


def get_user_permissions(user: User) -> List[str]:
    """
    Получает разрешения пользователя
    :param user: User
    :return: List[str]
    """
    permissions = list(map(
        lambda permission: permission.content_type.app_label + '.' + permission.codename,
        user.user_permissions.all()
    ))
    return permissions


def get_user_module_permissions(user: User) -> List[str]:
    """
    Получает список модулей в которых у пользователя есть разрешения
    :param user: User
    :return: List[str]
    """
    permissions = list(map(
        lambda perm: perm.content_type.app_label, user.user_permissions.all()
    ))
    return permissions
