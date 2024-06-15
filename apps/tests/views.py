# testing/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Ticket, Question, Theme
from .services import start_test, process_answer, get_question_with_answers
from django.http import JsonResponse
from django.urls import reverse

def start_test_view(request, ticket_id=None, theme_id=None):
    if ticket_id:
        ticket = get_object_or_404(Ticket, id=ticket_id)
        questions = start_test(ticket=ticket)
    elif theme_id:
        theme = get_object_or_404(Theme, id=theme_id)
        questions = start_test(theme=theme)
    else:
        questions = start_test()

    request.session['questions'] = [question.id for question in questions]
    request.session['current_question'] = 0
    request.session['correct_answers'] = 0
    request.session['incorrect_answers'] = 0
    request.session['question_status'] = [''] * len(questions)  # Initialize status
    request.session['answered_questions'] = []  # Initialize list for answered questions

    return redirect('testing:question')

def question_view(request):
    questions = request.session.get('questions', [])
    current_question = request.session.get('current_question', 0)
    if current_question >= len(questions):
        return redirect('testing:results')

    question_id = questions[current_question]
    question, answers = get_question_with_answers(question_id)
    question_status = request.session.get('question_status', [])
    indexed_status = list(enumerate(question_status))

    return render(request, 'testing/question.html', {
        'question': question,
        'answers': answers,
        'current_question': current_question + 1,
        'total_questions': len(questions),
        'indexed_status': indexed_status,
    })

def ajax_answer(request):
    if request.method == 'POST':
        questions = request.session.get('questions', [])
        current_question = request.session.get('current_question', 0)
        answered_questions = request.session.get('answered_questions', [])
        
        if current_question in answered_questions:
            return JsonResponse({'error': 'Question already answered'}, status=400)
        
        if current_question >= len(questions):
            return JsonResponse({'finished': True})

        question_id = questions[current_question]
        answer_id = request.POST.get('answer_id', '')
        is_correct, correct_answer = process_answer(question_id, answer_id)

        if is_correct:
            request.session['correct_answers'] += 1
            request.session['question_status'][current_question] = 'correct'
        else:
            request.session['incorrect_answers'] += 1
            request.session['question_status'][current_question] = 'incorrect'

        answered_questions.append(current_question)  # Add question to answered list
        request.session['answered_questions'] = answered_questions  # Update session with new list
        request.session['current_question'] += 1
        next_question_index = request.session['current_question']
        
        if next_question_index >= len(questions):
            return JsonResponse({'finished': True})

        next_question_id = questions[next_question_index]
        next_question, next_answers = get_question_with_answers(next_question_id)
        
        data = {
            'is_correct': is_correct,
            'correct_answers': request.session['correct_answers'],
            'incorrect_answers': request.session['incorrect_answers'],
            'current_question': next_question_index + 1,
            'total_questions': len(questions),
            'finished': False,
            'next_question_text': next_question.text_ru,
            'next_question_id': next_question.id,
            'next_answers': list(next_answers.values('id', 'text_ru')),
            'correct_answer': correct_answer,
            'question_status': request.session['question_status'],
        }
        return JsonResponse(data)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def navigate_question(request):
    if request.method == 'POST':
        question_index = int(request.POST.get('question_index', 0))
        questions = request.session.get('questions', [])
        if question_index >= len(questions):
            return JsonResponse({'error': 'Invalid question index'}, status=400)

        request.session['current_question'] = question_index
        question_id = questions[question_index]
        question, answers = get_question_with_answers(question_id)
        question_status = request.session.get('question_status', [])
        indexed_status = list(enumerate(question_status))

        data = {
            'current_question': question_index + 1,
            'next_question_text': question.text_ru,
            'next_question_id': question.id,
            'next_answers': list(answers.values('id', 'text_ru')),
            'correct_answers': request.session['correct_answers'],
            'incorrect_answers': request.session['incorrect_answers'],
            'question_status': indexed_status,
        }
        return JsonResponse(data)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def results_view(request):
    correct_answers = request.session.get('correct_answers', 0)
    incorrect_answers = request.session.get('incorrect_answers', 0)
    total_questions = len(request.session.get('questions', []))
    return render(request, 'testing/results.html', {
        'correct_answers': correct_answers,
        'incorrect_answers': incorrect_answers,
        'total_questions': total_questions,
    })
