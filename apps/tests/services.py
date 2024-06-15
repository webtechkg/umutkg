# testing/services.py
from .models import Question, Ticket, Theme
import random

def start_test(ticket=None, theme=None):
    if ticket:
        questions = list(Question.objects.filter(ticket=ticket))
    elif theme:
        questions = list(Question.objects.filter(theme=theme))
    else:
        questions = list(Question.objects.all())
        random.shuffle(questions)
    
    return questions

def process_answer(question_id, answer_id):
    question = Question.objects.get(id=question_id)
    answer = question.answers.get(id=answer_id)
    is_correct = answer.is_correct
    return is_correct, answer.text_ru

def get_question_with_answers(question_id):
    question = Question.objects.get(id=question_id)
    answers = question.answers.all()
    return question, answers
