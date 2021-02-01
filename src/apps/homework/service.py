import openpyxl
from django.db.models import QuerySet
from src.apps.neuro.answers import make_answer


def parse_questions(file_path):
    result = []
    workbook = openpyxl.open(file_path)
    sheet = workbook.worksheets[0]
    question_text_col = 'A'
    question_answer_col = 'B'
    num = 1
    for row in range(2, sheet.max_row + 1):
        text = sheet[question_text_col + str(row)].value
        answer = sheet[question_answer_col + str(row)].value
        if text and answer:
            result.append((num, text, str(answer).lower()))
            num += 1
    workbook.close()
    return result


def get_question_results(file):
    """Отправление файла к машинке и получение ответов"""
    return []


def get_homework_result(questions: QuerySet, file):
    """Получение ответов от машинки (пока заглушка)"""
    print('questions count {}'.format(questions.count()))
    answers = make_answer(questions.count(), file)
    print('answers')
    print(answers)
    has_answer_questions = []
    result = []
    for num in range(1, max(answers.answers.keys())):
        try:
            ans = (''.join(answers.answers.get(num, []))).lower()
            print('question {}, ans {}'.format(num, ans))
            question = questions.get(num=num)
            correct_answer = question.answer.lower()
            if ans and (ans in correct_answer or correct_answer in ans):
                ans = question.answer
            check = question.answer.lower() == ans
            result.append((question, ans, check))
            has_answer_questions.append(question)
        except Exception as e:
            print('get_homework_result error, number {}'.format(num))
            print(e)

    # Вопросы, на которые не было дано ответа
    for question in questions:
        if question not in has_answer_questions:
            result.append((question, '', False))
    return result, answers.data
