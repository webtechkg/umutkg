# testing/urls.py
from django.urls import path
from . import views

app_name = 'testing'
urlpatterns = [
    path('start_test/<int:ticket_id>/', views.start_test_view, name='start_test'),
    path('start_test/theme/<int:theme_id>/', views.start_test_view, name='start_test_theme'),
    path('question/', views.question_view, name='question'),
    path('results/', views.results_view, name='results'),
    path('ajax/answer/', views.ajax_answer, name='ajax_answer'),
    path('ajax/navigate/', views.navigate_question, name='navigate_question'),
]
