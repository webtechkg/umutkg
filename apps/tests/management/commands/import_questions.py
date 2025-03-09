import json
import os
from django.core.management.base import BaseCommand
from apps.tests.models import Ticket, Question, Answer  # Импорт моделей

from django.apps import apps

for model in apps.get_models():
    model.objects.all().delete()
    print(f"Все записи из {model.__name__} удалены!")

class Command(BaseCommand):
    help = "Импортирует вопросы из JSON в базу данных"

    def handle(self, *args, **kwargs):
        json_file_path = "parsed_questions.json"

        # Проверяем, существует ли файл
        if not os.path.exists(json_file_path):
            self.stdout.write(self.style.ERROR("Файл не найден!"))
            return

        with open(json_file_path, "r", encoding="utf-8") as file:
            data = json.load(file)  # Загружаем JSON

        for ticket_key, questions in data.items():
            ticket_number = int(ticket_key.split("_")[1])  # Получаем номер билета
            ticket, _ = Ticket.objects.get_or_create(number=ticket_number)  # Создаём билет

            for question_data in questions:
                question = Question.objects.create(
                    number=question_data["question_number"],
                    text_ru=question_data["question_text_ru"],
                    text_kg=question_data["question_text_kg"],
                    photo_url=question_data["image"] if question_data["image"] else None,
                    ticket=ticket,  # Привязываем к билету
                    theme=None  # Пока что нет данных о темах
                )

                # Создаём ответы
                for answer_ru, answer_kg in zip(question_data["answers_ru"], question_data["answers_kg"]):
                    Answer.objects.create(
                        question=question,
                        text_ru=answer_ru,
                        text_kg=answer_kg,
                        is_correct=False  # В JSON нет информации, какой ответ правильный
                    )

        self.stdout.write(self.style.SUCCESS("✅ Данные успешно импортированы!"))
