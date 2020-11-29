from typing import Union, Optional, NamedTuple, Tuple

from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email

from .models import User, RegistrationRequest
from django.contrib.auth import authenticate as auth, login
from src.quick_check import settings
from .models import user_type
from ..core.errors import ErrorMessages
from src.apps.core import service as server_service


class UserAuthData(NamedTuple):
    status: bool
    message: str
    user: Optional[User]


def get_user_by_email(email: str) -> Optional[User]:
    """
    Получение пользователя по email
    :param email: str
    :return: User or None
    """
    try:
        user = User.objects.get(email=email)
        return user
    except User.DoesNotExist:
        return None


def get_user_by_id(user_id: Union[str, int]) -> Optional[User]:
    """
    Получить пользователя по id
    :param user_id: str, int
    :return: User or None
    """
    try:
        user = User.objects.get(pk=user_id)
        return user
    except User.DoesNotExist:
        return None


def get_user_by_uuid(uuid: str) -> Optional[User]:
    """
    Получить пользователя по uuid
    :param uuid: str, int
    :return: User or None
    """
    try:
        user = User.objects.get(uuid=uuid)
        return user
    except User.DoesNotExist:
        return None


def authenticate(request, email: str, password: str) -> UserAuthData:
    """
    Авторизирует пользователя в системе
    :param request: request
    :param email: str
    :param password: str
    :return: UserAuthData = NamedTuple(status: bool, message: str, user: Optional[User]
    """
    user = auth(request, email=email, password=password)
    if not user:
        return UserAuthData(status=False, message=ErrorMessages.WRONG_EMAIL_OR_PASSWORD, user=None)
    login(request, user)
    return UserAuthData(status=True, message='', user=user)


def change_user_password(user: User, password: str) -> None:
    """
    Смена пароля пользователя
    :param user: User
    :param password: str
    :return: None
    """
    user.set_password(password)
    user.save()


def start_reset_password_session(user: User) -> None:
    """
    Начало сессии восстановления пароля пользователя
    :param user: User
    :return: bool - статус начала сессии
    """
    text = ('Забыли пароль?\n\n'
            'Ссылка для восстановления пароля:\n'
            '{}/{}'.format(server_service.get_site_url(), user.uuid)
            )
    send_mail('Восстановление пароля', text,
              from_email=settings.DEFAULT_FROM_EMAIL,
              recipient_list=[user.email])


def register_user(first_name: str, last_name: str, email: str, phone_number: str,
                  password: str, middle_name: str = '', registration_reason: str = '',
                  user_profile_type: int = user_type.PUPIL) -> Tuple[bool, str]:
    """
    Регистрация пользователя в системе

    :param user_profile_type: int
    :param first_name: str
    :param last_name: str
    :param email: str
    :param phone_number: str
    :param password: str
    :param middle_name: str
    :param registration_reason: str
    :return:
    """
    try:
        validate_email(email)
    except ValidationError:
        return False, ErrorMessages.WRONG_EMAIL
    user = get_user_by_email(email)
    if user:
        return False, ErrorMessages.EMAIL_EXISTS
    status = user_type.UserType.check_user_type(user_profile_type)
    if not status:
        return False, ErrorMessages.WRONG_USER_TYPE
    user = User.objects.create(email=email, first_name=first_name, last_name=last_name, middle_name=middle_name,
                               phone_number=phone_number, status=user_type)
    user.set_password(password)
    user.save()
    RegistrationRequest.objects.create(registration_user=user, registration_reason=registration_reason)
    return True, ''
