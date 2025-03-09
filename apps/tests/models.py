from django.db import models
from django.urls import reverse

# Create your models here.


class Ticket(models.Model):

    number = models.PositiveIntegerField("Номер вопроса")

    class Meta:
        verbose_name = ("Билет")
        verbose_name_plural = ("Билеты")

    def __str__(self):
        return f"Билет №{self.number}"


class Theme(models.Model):
    text = models.CharField("Название темы", max_length=255)
    photo = models.ImageField(upload_to='tests/theme', blank=True, null=True)
    desc = models.TextField("Описание темы", blank=True, null=True)

    class Meta:
        verbose_name = ("Тема")
        verbose_name_plural = ("Темы")

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})


class Question(models.Model):
    number = models.PositiveIntegerField("Номер вопроса")
    text_ru = models.TextField("Вопрос на русском")
    text_kg = models.TextField("Вопрос на кыргызском", blank=True, null=True)
    photo = models.ImageField(
        "Фото к вопросу", upload_to='tests/test', blank=True, null=True
    )
    photo_url = models.TextField("Фото к вопросу (URL)", blank=True, null=True)
    theme = models.ForeignKey(
        Theme, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Тема вопроса"
    )
    ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, verbose_name="Билет"
    )

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return self.text_ru

    def get_photo(self):
        """Возвращает либо локальное фото, либо URL"""
        if self.photo:
            return self.photo.url  # Используем локальное изображение
        else:
            return self.photo_url  # Используем внешний URL
        

class Answer(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers", verbose_name="Вопрос")
    text_ru = models.TextField("Ответ на русском")
    text_kg = models.TextField("Ответ на кыргызском", blank=True, null=True)
    is_correct = models.BooleanField("Правильный ли ответ?", default=False)

    class Meta:
        verbose_name = ("Ответ")
        verbose_name_plural = ("Ответы")

    def __str__(self):
        return self.text_ru
