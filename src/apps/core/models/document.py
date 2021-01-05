from django.db import models
from .safe_model import SafeModel
from django.utils.translation import gettext_lazy as _
from src.quick_check.settings import MEDIA_URL, SITE_METHOD, SITE_DOMAIN, SITE_PORT


class Document(SafeModel):
    """Модель документа, загружаемого в систему"""
    file = models.FileField()
    file_name = models.TextField(default='document')

    class Meta:
        db_table = 'documents'
        verbose_name_plural = _('Документы')
        verbose_name = _('Документ')

    @property
    def file_url(self):
        result = str(self.file).replace('\\', '/').split('/')[-1]
        return '{}://{}:{}{}'.format(SITE_METHOD, SITE_DOMAIN, SITE_PORT, MEDIA_URL + result)

    @property
    def display_file_name(self):
        return self.file_name

    def __str__(self):
        return self.file_name
