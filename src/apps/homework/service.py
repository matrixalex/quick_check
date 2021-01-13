from typing import List, Tuple

import openpyxl
from django.db.models import QuerySet
from src.apps.homework.models import Question
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


def get_homework_result(questions: QuerySet, file) -> List[Tuple[Question, str, bool]]:
    """Получение ответов от машинки (пока заглушка)"""
    print('questions count {}'.format(questions.count()))
    answers = make_answer(questions.count() * 2, file)
    has_answer_questions = []
    result = []
    print('answers')
    print(answers)
    for num, ans in enumerate(answers):
        try:
            question = questions.get(num=num + 1)
            check = question.answer == ans
            result.append((question, ans.lower(), check))
            has_answer_questions.append(question)
        except Exception as e:
            print('get_homework_result error')
            print(e)

    # Вопросы, на которые не было дано ответа
    for question in questions:
        if question not in has_answer_questions:
            result.append((question, '', False))
    return result
