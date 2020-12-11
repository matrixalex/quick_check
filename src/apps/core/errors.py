from django.utils.translation import gettext_lazy as _


class ErrorMessages:
    WRONG_EMAIL_OR_PASSWORD = _('Неправильно введен email или пароль')
    NO_USER = _('Пользователь не найден')
    PASSWORD_RESET_NOT_ACTIVE = _('Функция восстановления пароля отключена')
    WRONG_PASSWORD = _('Неправильно введен пароль')
    WRONG_EMAIL = _('Неправильно введен Email')
    EMAIL_EXISTS = _('Данный Email занят')
    WRONG_USER_TYPE = _('Некорректный тип учетной записи')
    USER_NOT_ACTIVE = _('Учетная запись не активирована')
    NO_USER_TYPE = _('Не найден тип учетной записи')
