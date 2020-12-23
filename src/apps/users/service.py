import uuid
from datetime import date
from typing import Union, Optional, NamedTuple, Tuple

from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email

from .models import User, RegistrationRequest, UserType
from django.contrib.auth import authenticate as auth, login
from src.quick_check import settings
from .models import user_type
from .serializers import UserSerializer
from ..core.errors import ErrorMessages
from src.apps.core import service as server_service
from ..core.models import Organization, StudyClass


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
                  password: str, birth_date: date, middle_name: str = '', registration_reason: str = '',
                  user_profile_type: int = user_type.PUPIL,
                  create_registration_request: bool = True,
                  is_accepted: bool = False, org: Organization = None) -> Tuple[bool, str]:
    """
    Регистрация пользователя в системе

    :param org: Organization
    :param is_accepted: bool
    :param create_registration_request: bool
    :param birth_date: date
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
    user_profile_type = get_user_type(user_profile_type)
    user = User.objects.create(email=email, first_name=first_name, last_name=last_name, middle_name=middle_name,
                               phone_number=phone_number, status=user_profile_type, birth_date=birth_date,
                               is_accepted=is_accepted)
    if not password:
        password = generate_random_password()
    user.set_password(password)
    user.save()
    if org:
        set_org(user, org)
    if create_registration_request:
        RegistrationRequest.objects.create(registration_user=user, registration_reason=registration_reason)
    return True, ''


def set_org(user: User, org: Organization):
    """Установить организацию пользователю"""
    user.org = org
    user.save()


def set_study_class(user: User, study_class: StudyClass):
    """Установить класс пользователю"""
    user.study_class = study_class
    user.save()


def change_user(user: User, first_name: str, last_name: str, email: str, phone_number: str, user_profile_type: UserType,
                password: str, birth_date: date, middle_name: str = '', org: Organization = None) -> Tuple[bool, str]:
    """Редактирование пользователя"""
    users = User.objects.filter(email=email)
    if user.email != email and users.exists():
        return False, ErrorMessages.EMAIL_EXISTS
    user.email = email
    user.first_name = first_name
    user.last_name = last_name
    user.phone_number = phone_number
    user.status = user_profile_type
    user.middle_name = middle_name
    user.birth_date = birth_date
    user.save()
    if password:
        user.set_password(password)
        user.save()
    if org:
        set_org(user, org)
    return True, ''


def get_user_type(user_type_id: int) -> Optional[UserType]:
    """Получить тип учетной записи по id"""
    try:
        return UserType.objects.get(pk=user_type_id)
    except UserType.DoesNotExist:
        return None


def generate_random_password() -> str:
    """Генерирует случайный пароль"""
    return str(uuid.uuid4())[-8:]


def serialize_user(user: User, short: bool = False) -> dict:
    """
    Сериализация пользователя.

    Если short=True, возвращает id, ФИО, тип учетной записи и флаг суперюзера
    """
    if short:
        return {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'middle_name': user.middle_name,
            'is_superuser': user.is_superuser,
            'user_type': user.status.name if user.status else '',
            'id': user.id
        }
    return UserSerializer(user).data
