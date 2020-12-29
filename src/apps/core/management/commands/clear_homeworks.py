from django.core.management import BaseCommand
from src.apps.homework.models import Homework, PupilHomework, Question, QuestionResult, HomeworkAppeal


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('deleting Homework')
        Homework.objects.all().delete()
        print('deleting PupilHomework')
        PupilHomework.objects.all().delete()
        print('deleting Question')
        Question.objects.all().delete()
        print('deleting QuestionResult')
        QuestionResult.objects.all().delete()
        print('deleting HomeworkAppeal')
        HomeworkAppeal.objects.all().delete()
        print('Success')
