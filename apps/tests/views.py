# testing/views.py
import random
from django.shortcuts import render, get_object_or_404, redirect
from .models import Ticket, Theme
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

    if len(questions) == 0:
        return render(request, "testing/tests.html", 
                     {"themes": Theme.objects.all(), 
                      "tickets": Ticket.objects.all(),
                      "error": "К сожалению, для этого билета/темы нет вопросов."})

    request.session["questions"] = [question.id for question in questions]
    request.session["current_question"] = 0
    request.session["correct_answers"] = 0
    request.session["incorrect_answers"] = 0
    request.session["question_status"] = [""] * len(questions)
    request.session["answered_questions"] = []

    return redirect("question")


def question_view(request):
    questions = request.session.get("questions", [])
    current_question = request.session.get("current_question", 0)
    # if current_question >= len(questions):
    #     return redirect("results")

    question_id = questions[current_question]
    question, answers = get_question_with_answers(question_id)
    question_status = request.session.get("question_status", [])
    indexed_status = list(enumerate(question_status))

    return render(
        request,
        "testing/question.html",
        {
            "question": question,
            "answers": answers,
            "current_question": current_question + 1,
            "total_questions": len(questions),
            "indexed_status": indexed_status,
        },
    )


def ajax_answer(request):
    if request.method == "POST":
        questions = request.session.get("questions", [])
        if not questions:
            return JsonResponse({"error": "Вопросы не найдены"}, status=400)

        current_question = request.session.get("current_question", 0)
        answered_questions = request.session.get("answered_questions", [])

        if current_question in answered_questions:
            return JsonResponse({"error": "Вопрос уже отвечен"}, status=400)

        if current_question >= len(questions):
            return JsonResponse({
                "finished": True,
                "correct_answers": request.session["correct_answers"],
                "incorrect_answers": request.session["incorrect_answers"],
                "total_questions": len(questions)
            })

        question_id = questions[current_question]
        answer_id = request.POST.get("answer_id", "")

        try:
            is_correct, correct_answer = process_answer(question_id, answer_id)
        except Exception as e:
            return JsonResponse({"error": f"Ошибка обработки ответа: {str(e)}"}, status=400)

        # Обновляем статус вопроса
        if is_correct:
            request.session["correct_answers"] += 1
            request.session["question_status"][current_question] = "correct"
        else:
            request.session["incorrect_answers"] += 1
            request.session["question_status"][current_question] = "incorrect"

        answered_questions.append(current_question)
        request.session["answered_questions"] = answered_questions
        request.session["current_question"] += 1
        next_question_index = request.session["current_question"]

        # Проверка на завершение теста
        if next_question_index >= len(questions):
            return JsonResponse({
                "finished": True,
                "correct_answers": request.session["correct_answers"],
                "incorrect_answers": request.session["incorrect_answers"],
                "total_questions": len(questions),
                "question_status": request.session["question_status"],
            })

        next_question_id = questions[next_question_index]
        try:
            next_question, next_answers = get_question_with_answers(next_question_id)
        except Exception as e:
            return JsonResponse({"error": f"Ошибка получения следующего вопроса: {str(e)}"}, status=400)

        # Используем photo_url, если photo отсутствует
        
        next_question_photo = next_question.photo.url if next_question.photo else next_question.photo_url

        data = {
            "is_correct": is_correct,
            "correct_answers": request.session["correct_answers"],
            "incorrect_answers": request.session["incorrect_answers"],
            "current_question": next_question_index + 1,
            "total_questions": len(questions),
            "finished": False,
            "next_question_text": next_question.text_ru,
            "next_question_id": next_question.id,
            "next_question_photo": next_question_photo,  # Передаём фото
            "next_answers": list(next_answers.values("id", "text_ru")),
            "correct_answer": correct_answer,
            "question_status": request.session["question_status"],
        }

        return JsonResponse(data)
    return JsonResponse({"error": "Неверный запрос"}, status=400)



def navigate_question(request):
    if request.method == "POST":
        question_index = int(request.POST.get("question_index", 0))
        questions = request.session.get("questions", [])
        if question_index >= len(questions):
            return JsonResponse({"error": "Invalid question index"}, status=400)

        request.session["current_question"] = question_index
        question_id = questions[question_index]
        question, answers = get_question_with_answers(question_id)
        question_status = request.session.get("question_status", [])
        indexed_status = list(enumerate(question_status))

        next_question_photo = question.photo.url if question.photo else question.photo_url
        data = {
            "current_question": question_index + 1,
            "next_question_text": question.text_ru,
            "next_question_id": question.id,
            "next_question_photo": next_question_photo,  # Передаем URL фотографии
            "next_answers": list(answers.values("id", "text_ru")),
            "correct_answers": request.session["correct_answers"],
            "incorrect_answers": request.session["incorrect_answers"],
            "question_status": indexed_status,
        }

        return JsonResponse(data)
    return JsonResponse({"error": "Invalid request"}, status=400)


def results_view(request):
    correct_answers = request.session.get("correct_answers", 0)
    incorrect_answers = request.session.get("incorrect_answers", 0)
    total_questions = len(request.session.get("questions", []))
    return render(
        request,
        "testing/results.html",
        {
            "correct_answers": correct_answers,
            "incorrect_answers": incorrect_answers,
            "total_questions": total_questions,
        },
    )


def list_themes_and_tickets_view(request):
    themes = Theme.objects.all()
    tickets = Ticket.objects.all()
    return render(
        request,
        "testing/tests.html",
        {"themes": themes, "tickets": tickets},
    )


def start_random_test_view(request):
    tickets = list(Ticket.objects.all())
    # themes = list(Theme.objects.all())
    # if random.choice([True, False]):
    random_ticket = random.choice(tickets)
    return redirect("start_test", ticket_id=random_ticket.id)
    # else:
    #     random_theme = random.choice(themes)
    #     return redirect("start_test_theme", theme_id=random_theme.id)


def toggle_language(request):
    if request.method == "POST":
        language = request.POST.get("language", "ru")
        current_question_index = int(request.POST.get("current_question", 0)) - 1

        questions = request.session.get("questions", [])
        question_id = questions[current_question_index]
        question, answers = get_question_with_answers(question_id)

        question_text = question.text_ru if language == "ru" else question.text_kg
        answers_data = [{"id": answer.id, "text": answer.text_ru if language == "ru" else answer.text_kg} for answer in answers]

        return JsonResponse({
            "question_text": question_text,
            "answers": answers_data,
        })

    return JsonResponse({"error": "Invalid request"}, status=400)
