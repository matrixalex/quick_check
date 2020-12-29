from django.db.models import Subquery, OuterRef, Count, Exists
from django.shortcuts import render
from django.views import View

from src.apps.core.api import BaseDeleteView, BaseCreateOrChangeView

from src.apps.homework.models import Homework, Question, HomeworkAppeal, PupilHomework, Criterion, MarkType, \
    QuestionResult
from src.apps.homework import service


class CreateOrChangeHomeworkView(BaseCreateOrChangeView):
    model = Homework
    _fields = {
        'name': {
            'type': BaseCreateOrChangeView.FieldTypeEnumerate.STR,
            'required': True
        },
        'description': {
            'type': BaseCreateOrChangeView.FieldTypeEnumerate.STR,
            'required': True
        },
        'homework_document': {
            'type': BaseCreateOrChangeView.FieldTypeEnumerate.FILE,
            'required': True,
            'validator': lambda document: (
                    document.file_name.split('.')[-1] and document.file_name.split('.')[-1] in ['csv', 'xlsx'])
        }
    }

    def before_post(self, request):
        return {
            'homework_teacher': request.user,
            'homework_criterion': Criterion.objects.filter(default=True).first(),
            'homework_marktype': MarkType.objects.filter(default=True).first()
        }

    def extra_post(self, request):
        pupils_id = request.data.get('pupils_id').split(',')
        questions_data = service.parse_questions(self.obj.homework_document.file)
        if questions_data:
            for pupil_id in pupils_id:
                PupilHomework.objects.create(pupil_id=pupil_id, homework_exercise=self.obj)
            for text, answer in questions_data:
                Question.objects.create(question_homework=self.obj, text=text, answer=answer)


class HomeWorkDeleteView(BaseDeleteView):
    model = Homework


class HomeworkShowView(View):
    @staticmethod
    def get(request, homework_id):
        data = {'user': request.user}
        homework = Homework.objects.get(pk=homework_id)
        pupil_homeworks = PupilHomework.objects.filter(homework_exercise=homework).select_related(
            'pupil'
        )
        for pupil_homework in pupil_homeworks:
            if HomeworkAppeal.objects.filter(parent=pupil_homework, is_deleted=False).exists():
                pupil_homework.appeal_id = HomeworkAppeal.objects.filter(
                    parent=pupil_homework,
                    is_deleted=False
                ).first().id
            else:
                pupil_homework.appeal_id = None
            pupil_homework.correct_count = QuestionResult.objects.filter(
                        pupil_homework=pupil_homework,
                        is_correct=True
                    ).count()
            pupil_homework.correct_count = Question.objects.filter(
                        question_homework=pupil_homework.homework_exercise
                    ).count()
        data['homework'] = homework
        data['pupil_homeworks'] = pupil_homeworks
        return render(request, 'teacher_homework.html', context=data)
