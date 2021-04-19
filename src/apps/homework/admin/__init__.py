from django.contrib.admin import site
from ..models import (
    Criterion, MarkType, Homework, PupilHomework, Question, HomeworkAppeal, QuestionResult, AppealResult, FontTemplate
)

site.register(Criterion)
site.register(MarkType)
site.register(Homework)
site.register(PupilHomework)
site.register(Question)
site.register(HomeworkAppeal)
site.register(QuestionResult)
site.register(AppealResult)
site.register(FontTemplate)
