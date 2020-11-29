from django.db import models
from src.apps.core.models import SafeModel
from django.utils.translation import gettext_lazy as _
from .user_type import UserType


class RegistrationStatus(models.IntegerChoices):
    """
    Класс статусов заявок на регистрацию
    """
    ACCEPTED = 0, _('Одобрена')
    NOT_ACCEPTED = 1, _('Отклонена')
    WAITING = 2, _('Ожидает подтверждения')


class RegistrationRequest(SafeModel):
    """Модель заявки на регистрацию"""
    registration_user = models.OneToOneField('users.User', on_delete=models.CASCADE,
                                             related_name='user_registration_request',
                                             verbose_name=_('Пользователь'))

    registration_reason = models.TextField(default='', verbose_name=_('Причина регистрации'))

    status = models.IntegerField(default=RegistrationStatus.WAITING, verbose_name=_('Статус одобрения'))

    class Meta:
        db_table = 'registration_requests'
        verbose_name = _('Заявка на регистрацию')
        verbose_name_plural = _('Заявки на регистрацию')

    def __str__(self):
        return 'Заявка на регистрацию {}: {}'.format(
            self.registration_user, self.registration_user.status
        )

    def save(self, *args, **kwargs):
        if self.status == RegistrationStatus.NOT_ACCEPTED:
            self.is_deleted = True
            self.registration_user.safe_delete()
        elif self.status == RegistrationStatus.ACCEPTED:
            self.is_deleted = True
            self.registration_user.accept_registration()
        super(RegistrationRequest, self).save(*args, **kwargs)
