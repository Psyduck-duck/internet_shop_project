from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact


def show_home(request):
    products = Product.objects.order_by('lust_change_date')[:5]
    return render(request, 'catalog/home.html', {'products': products})


def show_contacts(request):
    contacts = Contact.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        return HttpResponse(f'Спасибо, {name}! Ваше сообщение принято.')
    return render(request, 'catalog/contacts.html', {'contacts': contacts})
