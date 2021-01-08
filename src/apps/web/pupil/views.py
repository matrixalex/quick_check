import traceback

from django.shortcuts import render
from django.views import View
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView

from src.apps.core.errors import ErrorMessages
from src.apps.core.service import upload_file
from src.apps.homework.models import PupilHomework, Question, QuestionResult, HomeworkAppeal, AppealResult
from src.apps.homework.service import get_homework_result
from src.apps.users.models import user_type


class UploadHomeworkView(APIView):
    """Загрузка домашней работы учеником."""

    def process_request(self, request):
        homework_id = request.data.get('homework_id')
        homework = PupilHomework.objects.get(pk=homework_id)
        file = request.data.get('file')
        document = upload_file(file)
        questions = Question.objects.filter(question_homework__pupil_homework_exercise=homework)
        answers = get_homework_result(questions, str(document.file))
        count = 0
        for question, answer, check in answers:
            QuestionResult.objects.create(
                pupil_homework=homework,
                homework_question=question,
                answer=answer,
                is_correct=check
            )
            if check:
                count += 1
        mark = homework.homework_exercise.homework_criterion.get_mark(count / questions.count())
        homework.pupilhomework_document = document
        homework.status = PupilHomework.UPLOADED_HAS_ANSWER
        homework.mark = mark
        homework.save()

    def post(self, request):
        try:
            self.process_request(request)
        except Exception as e:
            print('core exception')
            traceback.print_exc(e)
            return Response({'result': {'message': ErrorMessages.UNHANDLED}}, HTTP_400_BAD_REQUEST)
        return Response({'result': {'message': ''}}, HTTP_200_OK)


class PupilHomeworkShowView(View):
    @staticmethod
    def get(request, homework_id):
        user = request.user
        homework = PupilHomework.objects.select_related(
            'pupilhomework_document',
            'homework_exercise'
        ).get(pk=homework_id)
        data = {'user': user, 'homework': homework}
        question_results = QuestionResult.objects.filter(
            pupil_homework=homework
        ).select_related('homework_question').order_by('homework_question__num')
        no_answer_questions = Question.objects.filter(question_homework__pupil_homework_exercise=homework).exclude(
            questionresult_homework_question__in=question_results
        )
        no_answer_questions_count = no_answer_questions.count()
        data['question_results'] = question_results
        data['is_teacher'] = request.user.status.id == user_type.TEACHER
        data['correct_answers_count'] = question_results.filter(is_correct=True).count()
        data['bad_answers_count'] = question_results.filter(is_correct=False).count() + no_answer_questions_count
        data['no_answer_questions'] = no_answer_questions
        data['all_count'] = question_results.count() + no_answer_questions_count
        return render(request, 'pupil_homework.html', context=data)


class AppealHomeworkView(APIView):
    @staticmethod
    def post(request):
        homework_id = request.data.get('homework_id')
        homework = PupilHomework.objects.get(pk=homework_id)
        file = request.data.get('file')
        document = upload_file(file)
        text = request.data.get('text')
        appeal = HomeworkAppeal.objects.create(
            parent=homework,
            homeworkappeal_document=document,
            text=text
        )
        return Response({'result': {'message': ''}}, HTTP_200_OK)


class AppealResultView(APIView):
    @staticmethod
    def get(request, appeal_result_id):
        appeal_result = AppealResult.objects.get(pk=appeal_result_id)
        return Response({'result': {'text': appeal_result.text}}, HTTP_200_OK)

    @staticmethod
    def post(request, appeal_result_id):
        appeal_result = AppealResult.objects.get(pk=appeal_result_id)
        appeal_result.parent.is_deleted = True
        appeal_result.parent.save()
        appeal_result.is_deleted = True
        appeal_result.save()
        return Response({'result': {'message': ''}}, HTTP_200_OK)
