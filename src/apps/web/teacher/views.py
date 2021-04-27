from django.db.models import Subquery, OuterRef, Count, Exists
from django.shortcuts import render
from django.views import View
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from src.apps.core.api import BaseDeleteView, BaseCreateOrChangeView

from src.apps.homework.models import Homework, Question, HomeworkAppeal, PupilHomework, Criterion, MarkType, \
    QuestionResult, AppealResult
from src.apps.homework import service


class CreateOrChangeHomeworkView(BaseCreateOrChangeView):
    model = Homework
    criterion = None
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
                    document.file_name.split('.')[-1] and document.file_name.split('.')[-1]
                    in ['csv', 'xlsx', 'pdf', 'jpeg', 'png', 'svg', 'docx', 'txt'])
        }
    }

    def before_post(self, request):
        print('before post')
        criterion_id = int(request.data.get('criterion_id'))
        self.criterion = Criterion.objects.get(id=criterion_id)
        return {
            'homework_teacher': request.user,
            'homework_criterion': self.criterion,
            'homework_marktype': MarkType.objects.filter(default=True).first(),
        }

    def extra_post(self, request):
        print('extra post')
        pupils_id = request.data.get('pupils_id').split(',')
        if self.criterion.criterion_type == self.criterion.KEY_TYPE:
            questions_data = service.parse_questions(str(self.obj.homework_document.file))
            if questions_data:
                for pupil_id in pupils_id:
                    PupilHomework.objects.create(pupil_id=pupil_id, homework_exercise=self.obj)
                for num, text, answer in questions_data:
                    Question.objects.create(question_homework=self.obj, text=text, answer=answer, num=num)
        else:
            text = service.parse_text(str(self.obj.homework_document.file))
            for pupil_id in pupils_id:
                PupilHomework.objects.create(pupil_id=pupil_id, homework_exercise=self.obj)
            Question.objects.create(question_homework=self.obj, text=text, answer=text, num=1)


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
            pupil_homework.all_count = Question.objects.filter(
                        question_homework=pupil_homework.homework_exercise
                    ).count()
        data['homework'] = homework
        data['pupil_homeworks'] = pupil_homeworks
        return render(request, 'teacher_homework.html', context=data)


class AppealHomeworkView(APIView):
    @staticmethod
    def post(request):
        homework_id = request.data.get('homework_id')
        text = request.data.get('text')
        appeal_id = request.data.get('appeal_id')
        appeal = HomeworkAppeal.objects.get(pk=appeal_id)
        homework = PupilHomework.objects.get(pk=homework_id)
        AppealResult.objects.create(parent=appeal, pupil_homework=homework, text=text)
        appeal.is_deleted = True
        appeal.save()
        homework.status = PupilHomework.UPLOADED_HAS_ANSWER
        homework.save()
        return Response({'result': {'message': ''}}, HTTP_200_OK)


class HomeworkAppealShowView(View):
    @staticmethod
    def get(request, appeal_id):
        user = request.user
        appeal = HomeworkAppeal.objects.select_related(
            'parent',
            'homeworkappeal_document'
        ).get(pk=appeal_id)
        data = {'user': user, 'appeal': appeal}
        return render(request, 'teacher_appeal.html', context=data)
