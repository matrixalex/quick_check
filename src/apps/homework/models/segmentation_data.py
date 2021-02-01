from django.db import models
from src.apps.core.models import SafeModel


class SegmentationData(SafeModel):
    x_start = models.IntegerField(default=0)
    y_start = models.IntegerField(default=0)
    x_end = models.IntegerField(default=0)
    y_end = models.IntegerField(default=0)
    pupil_homework = models.ForeignKey('homework.PupilHomework', on_delete=models.CASCADE)
    answer = models.TextField(default='')