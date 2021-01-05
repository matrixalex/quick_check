from typing import List, NamedTuple, Tuple

import openpyxl
from django.db.models import QuerySet

from src.apps.homework.models import Question


def parse_questions(file_path):
    result = []
    workbook = openpyxl.open(file_path)
    sheet = workbook.worksheets[0]
    question_text_col = 'A'
    question_answer_col = 'B'
    num = 1
    for row in range(1, sheet.max_row + 1):
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
    # answers = get_question_results(file)
    answers = [(i, 'default') for i in range(1, questions.count() + 1)]
    answers.sort(key=lambda item: item[0])
    has_answer_questions = []
    result = []
    for num, ans in answers:
        question = questions.get(num=num)
        check = question.answer == ans
        result.append((question, ans.lower(), check))
        has_answer_questions.append(question)

    # Вопросы, на которые не было дано ответа
    for question in questions:
        if question not in has_answer_questions:
            result.append((question, '', False))
    return result
