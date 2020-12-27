from src.apps.core.models import SafeModel
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserLog(SafeModel):
    log_user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='userlog_user',
                                 verbose_name=_('Пользователь'))
    text = models.TextField(default='', verbose_name=_('Текст'))

    class Meta:
        db_table = 'user_logs'
        verbose_name_plural = _('Логи пользователей')
        verbose_name = _('Лог пользователя')
        ordering = ['log_user', '-created_at']
