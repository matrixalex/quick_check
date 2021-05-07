import datetime
from datetime import datetime, date
from typing import Optional, Union

from django.db.models import QuerySet
from django.shortcuts import render
from django.utils import timezone
from src.quick_check import settings
from .models import Document, Organization, StudyClass
import uuid
import os

from ..homework.models import Homework
from ..users.models import User


def get_time_now() -> datetime:
    """
    Получить текущее серверное время
    :return: datetime
    """
    return timezone.now()


def parse_date(date_str: str) -> date:
    result = datetime.strptime(date_str, '%Y-%m-%d')
    return result


def upload_file(file_object) -> Document:
    """Загрузка файла"""
    if isinstance(file_object, str):
        file_name = file_object.replace('\\', '/').split('/')[-1]
        return Document.objects.create(file=file_object, file_name=file_name)
    else:
        file_name = '{}.{}'.format(uuid.uuid4(), file_object.name.split('.')[-1])
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        with open(file_path, 'wb+') as file:
            for chunk in file_object.chunks():
                file.write(chunk)
        try:
            return Document.objects.create(file=file_path, file_name=file_object.name)
        except Exception as e:
            print(repr(e))


def get_all_orgs() -> QuerySet:
    """Получить все организации"""
    return Organization.objects.all()


def get_org_by_id(org_id: int) -> Optional[Organization]:
    """Получить организацию по id"""
    try:
        return Organization.objects.get(pk=org_id)
    except Organization.DoesNotExist:
        return None


def create_org(name: str) -> Organization:
    """Создание организации"""
    org = Organization.objects.create(name=name)
    return org


def change_org(org: Union[int, Organization], name: str) -> Organization:
    """Редактирование организации"""
    if not isinstance(org, Organization):
        org = get_org_by_id(org)
    if org:
        org.name = name
        org.save()
    return org


def delete_org(org: Union[int, Organization]) -> None:
    if not isinstance(org, Organization):
        org = get_org_by_id(org)
    if org:
        org.safe_delete()


def get_site_url() -> str:
    """Получение текущего url сайта"""
    return '{}://{}:{}'.format(settings.SITE_METHOD, settings.SITE_DOMAIN, settings.SITE_PORT)


def render_error(request, message):
    """Рендер страницы ошибки"""
    return render(request, 'error.html', context={'message': message})


def get_study_class_by_id(study_class_id: Union[str, int]) -> Optional[StudyClass]:
    """Получить класс по id."""
    try:
        study_class = StudyClass.objects.get(pk=study_class_id)
        return study_class
    except StudyClass.DoesNotExist:
        return None


def get_study_classes(org: Organization = None) -> QuerySet:
    """Получить список классов по организации"""
    if org:
        return StudyClass.objects.filter(org=org)
    return StudyClass.objects.all()


def search_user(user_str: str, teacher: User = None, homework: Homework = None) -> Optional[User]:
    names = user_str.split()
    last_name = names[0].lower()
    first_name = names[1].lower()
    middle_name = names[2].lower()
    users = User.objects.filter(
        last_name__iexact=last_name,
        first_name__iexact=first_name,
        middle_name__iexact=middle_name
    )
    if teacher:
        users = users.filter(study_class__teachers__in=[teacher])
    if homework:
        users = users.filter(pupil_homework_pupil__homework_exercise=homework)
    if users.exists:
        return users.first()
    return None
