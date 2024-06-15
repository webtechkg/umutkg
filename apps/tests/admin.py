# testing/admin.py
from django.contrib import admin
from .models import Theme, Question, Answer, Ticket


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('number', 'text_ru', 'theme')
    list_filter = ('theme',)
    search_fields = ('text_ru', 'text_kg')
    inlines = [AnswerInline]


class ThemeAdmin(admin.ModelAdmin):
    list_display = ('text', 'desc')
    search_fields = ('text', 'desc')


class TicketAdmin(admin.ModelAdmin):
    list_display = ('number',)
    


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('text_ru', 'text_kg', 'is_correct')
    list_filter = ('is_correct',)
    search_fields = ('text_ru', 'text_kg')


admin.site.register(Theme, ThemeAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Answer, AnswerAdmin)
