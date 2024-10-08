from django.shortcuts import render
from apps.tests.models import Ticket, Theme


# Create your views here.


def main(request):
    themes = Theme.objects.all()
    tickets = Ticket.objects.all()
    context = {"themes": themes, "tickets": tickets}
    return render(request, 'main/home.html', context)


def contact(request):
    return render(request, 'main/page-contact.html')
