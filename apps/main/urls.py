from django.urls import path
from .views import main, contact

urlpatterns = [
    path('', main, name='home'),
    path('contact/', contact, name='contact'),
]
