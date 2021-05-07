from django.shortcuts import render
from django.utils.html import format_html
from django.views import View
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from src.apps.core.service import upload_file, get_site_url
from src.apps.homework.models import PupilHomework, Question, QuestionResult, HomeworkAppeal, AppealResult, \
    FontTemplate, Criterion, SegmentationData
from src.apps.homework.service import SequenceAlignment, get_homework_result
from src.apps.users.models import user_type


def parse_text_neuro(file_path):
    return 'same_text'


def get_text_homework_result(file_path, correct_text):
    text = parse_text_neuro(file_path)
    align = SequenceAlignment(correct_text, text)
    mistake_count, mistakes = align.alignment()
    return text, mistake_count


def handle_homework_upload(homework: PupilHomework, document):
    if homework.homework_exercise.homework_criterion.criterion_type == Criterion.KEY_TYPE:
        questions = Question.objects.filter(question_homework__pupil_homework_exercise=homework)
        homework_result = get_homework_result(questions, str(document.file))
        count = 0
        for question, answer, check in homework_result[0]:
            QuestionResult.objects.create(
                pupil_homework=homework,
                homework_question=question,
                answer=answer,
                is_correct=check
            )
            if check:
                count += 1
        mark = homework.homework_exercise.homework_criterion.get_mark(count / questions.count())
        for segment_data in homework_result[1]:
            SegmentationData.objects.create(
                x_start=segment_data[0],
                y_start=segment_data[1],
                x_end=segment_data[2],
                y_end=segment_data[3],
                answer=segment_data[4],
                pupil_homework=homework
            )
    else:
        question = Question.objects.filter(question_homework__pupil_homework_exercise=homework).first()
        text, mistake_count = get_text_homework_result(str(document.file), question.answer)
        mark = homework.homework_exercise.homework_criterion.get_mark(mistake_count)
        homework.mistake_count = mistake_count
        QuestionResult.objects.create(
            pupil_homework=homework,
            homework_question=question,
            answer=text,
            is_correct=True
        )
    homework.pupilhomework_document = document
    homework.status = PupilHomework.UPLOADED_HAS_ANSWER
    homework.mark = mark
    homework.save()


class UploadHomeworkView(APIView):
    """Загрузка домашней работы учеником."""

    def process_request(self, request):
        homework_id = request.data.get('homework_id')
        homework = PupilHomework.objects.get(pk=homework_id)
        file = request.data.get('file')
        document = upload_file(file)
        handle_homework_upload(homework, document)

    def post(self, request):
        # try:
        self.process_request(request)
        #except Exception as e:
        #    print('core exception')
        #    traceback.print_exc(e)
        #    return Response({'result': {'message': ErrorMessages.UNHANDLED}}, HTTP_400_BAD_REQUEST)
        return Response({'result': {'message': ''}}, HTTP_200_OK)


class PupilHomeworkShowView(View):
    @staticmethod
    def get(request, homework_id):
        user = request.user
        homework = PupilHomework.objects.select_related(
            'pupilhomework_document',
            'homework_exercise'
        ).get(pk=homework_id)
        data = {'user': user, 'homework': homework, 'is_teacher': request.user.status.id == user_type.TEACHER}
        question_results = QuestionResult.objects.filter(
            pupil_homework=homework
        ).select_related('homework_question').order_by('homework_question__num')
        data['question_results'] = question_results
        if homework.homework_exercise.homework_criterion.criterion_type == Criterion.KEY_TYPE:
            no_answer_questions = Question.objects.filter(question_homework__pupil_homework_exercise=homework).exclude(
                questionresult_homework_question__in=question_results
            )
            no_answer_questions_count = no_answer_questions.count()
            data['correct_answers_count'] = question_results.filter(is_correct=True).count()
            data['bad_answers_count'] = question_results.filter(is_correct=False).count() + no_answer_questions_count
            data['no_answer_questions'] = no_answer_questions
            data['all_count'] = question_results.count() + no_answer_questions_count
        else:
            pupil_question = question_results.first()
            question = pupil_question.homework_question
            pupil_text = pupil_question.answer
            correct_text = question.answer
            data['pupil_text'] = pupil_text
            data['correct_text'] = correct_text
            if homework.mistake_count != 0:
                pupil_text = list(pupil_text)
                align = SequenceAlignment(correct_text, pupil_text)
                mistake_count, mistakes = align.alignment()
                for i, mistake_flag in enumerate(mistakes):
                    try:
                        if mistake_flag:
                            pupil_text[i] = '<b>{}</b>'.format(pupil_text[i])
                    except:
                        pass
                pupil_text = ''.join(pupil_text)
                data['pupil_text'] = format_html(pupil_text)
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


class TemplateView(View):
    @staticmethod
    def get(request):
        user = request.user
        templates = FontTemplate.objects.filter(hidden_homework__pupil=user)
        numeric_flag = templates.filter(template_type=FontTemplate.NUMERIC).exists()
        cyrillic_flag = templates.filter(template_type=FontTemplate.CYRILLIC).exists()
        latin_flag = templates.filter(template_type=FontTemplate.LATIN).exists()
        numeric_url = get_site_url() + FontTemplate.TEMPLATE_PATHS[FontTemplate.NUMERIC]
        cyrillic_url = get_site_url() + FontTemplate.TEMPLATE_PATHS[FontTemplate.CYRILLIC]
        latin_url = get_site_url() + FontTemplate.TEMPLATE_PATHS[FontTemplate.LATIN]
        data = {
            'user': user,
            'numeric_flag': numeric_flag,
            'cyrillic_flag': cyrillic_flag,
            'latin_flag': latin_flag,
            'numeric_url': numeric_url,
            'cyrillic_url': cyrillic_url,
            'latin_url': latin_url,
        }
        return render(request, 'templates.html', context=data)


class TemplateUploadView(APIView):
    def post(self, request):
        template_type = int(request.data.get('template_type'))
        file = request.data.get('file')
        doc = upload_file(file)
        homework = PupilHomework.objects.create(pupil=request.user, pupilhomework_document=doc, is_hidden=True)
        FontTemplate.objects.create(template_type=template_type, hidden_homework=homework)
        user = request.user
        user.is_any_template_uploaded = True
        user.save()
        return Response(data={'success': True}, status=HTTP_200_OK)
