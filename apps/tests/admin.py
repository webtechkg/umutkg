from django.contrib import admin
from .models import Theme, Question, Answer, Ticket


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4


class QuestionInline(admin.TabularInline):  # Встраиваем вопросы в билет
    model = Question
    extra = 1  # Количество пустых форм для новых вопросов
    show_change_link = True  # Позволяет переходить к редактированию вопроса из билета


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('number', 'text_ru', 'theme', 'ticket')
    list_filter = ('theme', 'ticket')
    search_fields = ('text_ru', 'text_kg')
    inlines = [AnswerInline]


class ThemeAdmin(admin.ModelAdmin):
    list_display = ('text', 'desc')
    search_fields = ('text', 'desc')


class TicketAdmin(admin.ModelAdmin):
    list_display = ('number',)
    inlines = [QuestionInline]  # Добавляем вопросы в страницу билета


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('text_ru', 'text_kg', 'is_correct', 'question')
    list_filter = ('is_correct',)
    search_fields = ('text_ru', 'text_kg')


admin.site.register(Theme, ThemeAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Answer, AnswerAdmin)
