from django.shortcuts import render
from django.http import HttpResponse


def show_home(request):
    return render(request, 'catalog/home.html')


def show_contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        return HttpResponse(f'Спасибо, {name}! Ваше сообщение принято.')
    return render(request, 'catalog/contacts.html')
