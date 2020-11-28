from django.db import models
from .safe_model import SafeModel
from src.quick_check import settings


class Document(SafeModel):
    file = models.FileField()
    file_name = models.TextField

    @property
    def file_url(self):
        print(self.file)
        return self.file

    def __str__(self):
        return self.file_name
