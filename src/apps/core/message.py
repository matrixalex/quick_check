from django.utils.translation import gettext_lazy as _


class InfoMessage:
    """Класс информирующих сообщений"""
    REGISTRATION_SUCCESS = _('Вы успешно зарегистрировались! Дождитесь одобрения регистрации')


class DataInfoMessage(InfoMessage):
    """Класс информирующих сообщений, предполагающий вставку данных"""
    REGISTRATION_SUCCESS = _('Вы успешно зарегистрировались как "{}", дождитесь, пока "{}" одобрит вашу заявку')
