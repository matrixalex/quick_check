from django.contrib.admin import site
from ..models import (
    Criterion, MarkType, Homework, HomeworkResult, PupilHomework, Question, QuestionAppeal, QuestionResult
)

site.register(Criterion)
site.register(MarkType)
site.register(Homework)
site.register(HomeworkResult)
site.register(PupilHomework)
site.register(Question)
site.register(QuestionAppeal)
site.register(QuestionResult)
