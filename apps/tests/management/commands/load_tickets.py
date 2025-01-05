import json
import os

from django.core.management.base import BaseCommand

from apps.tests.models import Answer, Question, Theme, Ticket


class Command(BaseCommand):
    help = "Загрузка данных билетов и вопросов из JSON-файла в базу данных"

    def add_arguments(self, parser):
        parser.add_argument(
            "--file", type=str, help="Путь к JSON-файлу с данными", required=True
        )

    def handle(self, *args, **kwargs):
        file_path = kwargs["file"]

        if not os.path.exists(file_path):
            self.stderr.write(f"Файл {file_path} не найден.")
            return

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except json.JSONDecodeError as e:
            self.stderr.write(f"Ошибка чтения JSON: {e}")
            return

        for ticket_data in data:
            ticket_number = ticket_data.get("ticket_number")
            questions = ticket_data.get("questions", [])

            if not ticket_number:
                self.stderr.write(f"Пропущен билет из-за отсутствия номера.")
                continue

            # Создание или получение билета
            ticket, _ = Ticket.objects.get_or_create(number=ticket_number)

            for question_data in questions:
                question_number = question_data.get("question_number")
                question_text = question_data.get("question_text")
                image_url = question_data.get("image_url")
                answers_data = question_data.get("answers", [])

                if not question_text or not question_number:
                    self.stderr.write(f"Пропущен вопрос из-за отсутствия данных.")
                    continue

                # Создание или получение темы
                theme, _ = Theme.objects.get_or_create(
                    text="Общая тема",  # Укажите тему, если она общая
                )

                # Создание вопроса
                question = Question.objects.create(
                    number=question_number,
                    text_ru=question_text,
                    ticket=ticket,
                    theme=theme,
                )

                # Сохранение фото, если есть
                if image_url:
                    question.photo = (
                        image_url  # Замените на обработку, если нужно скачивать
                    )
                    question.save()

                # Создание ответов
                for answer_text in answers_data:
                    Answer.objects.create(
                        question=question,
                        text_ru=answer_text,
                        is_correct=False,  # Укажите правильные ответы, если информация есть
                    )

        self.stdout.write(self.style.SUCCESS("Данные успешно загружены в базу данных."))
