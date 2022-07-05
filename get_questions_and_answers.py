import os
import re


def get_questions_files() -> str:
    all_texts = ""
    for filename in os.listdir(os.path.join(os.getcwd(), 'quiz-questions')):
        with open(os.path.join(
                os.getcwd(),
                os.path.join('quiz-questions', filename)
        ), 'r', encoding='KOI8-R') as questions_file:
            questions_file_contents = questions_file.read()
        all_texts += questions_file_contents
    return all_texts


def find_text(pattern, paragraph):
    match = re.match(pattern, paragraph)
    if match:
        return paragraph[len(match.group()):]


def get_quiz_bank() -> dict:
    quiz_bank = {}
    question_pattern = r'Вопрос \d+:\n'
    answer_pattern = r'Ответ:\n'
    all_texts = get_questions_files()
    paragraphs = all_texts.split('\n\n')
    question, answer = None, None
    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if question is None:
            question = find_text(question_pattern, paragraph)
        if answer is None:
            answer = find_text(answer_pattern, paragraph)
        if question and answer:
            question = question.replace("\n", " ")
            answer = answer.replace("\n", " ")
            quiz_bank[question] = answer
            question, answer = None, None

    return quiz_bank
