from datetime import datetime
from django.utils import timezone
from src.quick_check import settings
from .models import Document
import uuid
import os


def get_time_now() -> datetime:
    """
    Получить текущее серверное время
    :return: datetime
    """
    return timezone.now()


def upload_file(file_object) -> Document:
    """Загрузка файла"""
    file_name = '{}.{}'.format(uuid.uuid4(), file_object.name.split('.')[-1])
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    with open(file_path, 'wb+') as file:
        for chunk in file_object.chunks():
            file.write(chunk)
        document = Document.objects.create(file=file, file_name=file_object.name)
        return document


def get_site_url() -> str:
    """Получение текущего url сайта"""
    return '{}://{}'.format(settings.SITE_METHOD, settings.SITE_DOMAIN)
