from django.db import models
from django.urls import reverse

# Create your models here.


class Theme(models.Model):
    text = models.CharField("Название темы", max_length=255)
    photo = models.ImageField(upload_to='tests/theme')
    desc = models.TextField("Описание темы")

    class Meta:
        verbose_name = ("Тема")
        verbose_name_plural = ("Темы")

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})


class Question(models.Model):

    number = models.PositiveIntegerField("Номер вопроса")
    text_ru = models.TextField("Текст Вопроса")
    text_kg = models.TextField("Вопросдын тексты")
    photo = models.ImageField(upload_to='tests/test', blank=True, null=True)
    theme = models.ForeignKey(
        Theme, on_delete=models.CASCADE, verbose_name="Тема вопроса")

    class Meta:
        verbose_name = ("Вопрос")
        verbose_name_plural = ("Вопросы")

    def __str__(self):
        return self.text_ru

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})


class Answer(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers", verbose_name="Вопрос")
    text_ru = models.TextField("Ответ на русском")
    text_kg = models.TextField("Ответ на кыргызском")
    is_correct = models.BooleanField("Правильный ли ответ?", default=False)

    class Meta:
        verbose_name = ("Ответ")
        verbose_name_plural = ("Ответы")

    def __str__(self):
        return self.text_ru


class Ticket(models.Model):

    number = models.PositiveIntegerField("Номер вопроса")
    questions = models.ManyToManyField(Question, verbose_name="Вопрос")

    class Meta:
        verbose_name = ("Билет")
        verbose_name_plural = ("Билеты")

    def __str__(self):
        return f"Билет №{self.number}"

