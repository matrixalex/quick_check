import openpyxl


def parse_questions(file_path):
    result = []
    workbook = openpyxl.open(file_path)
    sheet = workbook.worksheets[0]
    question_text_col = 'A'
    question_answer_col = 'B'
    for row in range(1, sheet.max_row + 1):
        text = sheet[question_text_col + str(row)].value
        answer = sheet[question_answer_col + str(row)].value
        if text and answer:
            result.append((text, str(answer).lower()))
    workbook.close()
    return result
